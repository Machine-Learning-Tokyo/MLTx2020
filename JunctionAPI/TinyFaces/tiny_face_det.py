# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf
import tiny_face_model
import JunctionAPI.TinyFaces.util
import numpy as np
import cv2

import time
from scipy.special import expit


def overlay_bounding_boxes(raw_img, refined_bboxes, lw):
    # Overlay bounding boxes on an image with the color based on the confidence.
    for r in refined_bboxes:
        _score = expit(r[4])
        cm_idx = int(np.ceil(_score * 255))
        rect_color = [int(np.ceil(x * 255)) for x in JunctionAPI.TinyFaces.util.cm_data[cm_idx]]  # parula
        _lw = lw
        if lw == 0:  # line width of each bounding box is adaptively determined.
            bw, bh = r[2] - r[0] + 1, r[3] - r[0] + 1
            _lw = 1 if min(bw, bh) <= 20 else max(2, min(3, min(bh / 20, bw / 20)))
            _lw = int(np.ceil(_lw * _score))

        _r = [int(x) for x in r[:4]]
        cv2.rectangle(raw_img, (_r[0], _r[1]), (_r[2], _r[3]), rect_color, _lw)


def evaluate(img_path, prob_thresh=0.5, nms_thresh=0.1, lw=3, display=False):
    x = tf.placeholder(tf.float32, [1, None, None, 3])  # n, h, w, c
    model = tiny_face_model.Model('/path/to/pkl/file/')
    score_final = model.tiny_face(x)


    average_image = model.get_data_by_key("average_image")
    clusters = model.get_data_by_key("clusters")

    # main
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        fname   = img_path
        raw_img = cv2.imread(img_path)
        raw_img = cv2.cvtColor(raw_img, cv2.COLOR_BGR2RGB)
        raw_img_f = raw_img.astype(np.float32)

        scales = [0.5, 1, 1.5, 2.0]
        start = time.time()

        # initialize output
        bboxes = np.empty(shape=(0, 5))

        # process input at different scales
        for s in scales:
            print("Processing {} at scale {:.4f}".format(fname, s))
            img = cv2.resize(raw_img_f, (0, 0), fx=s, fy=s, interpolation=cv2.INTER_LINEAR)
            img = img - average_image
            img = img[np.newaxis, :]

            # we don't run every template on every scale ids of templates to ignore
            tids = list(range(4, 12)) + ([] if s <= 1.0 else list(range(18, 25)))
            ignoredTids = list(set(range(0, clusters.shape[0])) - set(tids))

            # run through the net
            score_final_tf = sess.run(score_final, feed_dict={x: img})

            # collect scores
            score_cls_tf, score_reg_tf = score_final_tf[:, :, :, :25], score_final_tf[:, :, :, 25:125]
            prob_cls_tf = expit(score_cls_tf)
            prob_cls_tf[0, :, :, ignoredTids] = 0.0

            def _calc_bounding_boxes():
                # threshold for detection
                _, fy, fx, fc = np.where(prob_cls_tf > prob_thresh)

                # interpret heatmap into bounding boxes
                cy = fy * 8 - 1
                cx = fx * 8 - 1
                ch = clusters[fc, 3] - clusters[fc, 1] + 1
                cw = clusters[fc, 2] - clusters[fc, 0] + 1

                # extract bounding box refinement
                Nt = clusters.shape[0]
                tx = score_reg_tf[0, :, :, 0:Nt]
                ty = score_reg_tf[0, :, :, Nt:2 * Nt]
                tw = score_reg_tf[0, :, :, 2 * Nt:3 * Nt]
                th = score_reg_tf[0, :, :, 3 * Nt:4 * Nt]

                # refine bounding boxes
                dcx = cw * tx[fy, fx, fc]
                dcy = ch * ty[fy, fx, fc]
                rcx = cx + dcx
                rcy = cy + dcy
                rcw = cw * np.exp(tw[fy, fx, fc])
                rch = ch * np.exp(th[fy, fx, fc])

                scores = score_cls_tf[0, fy, fx, fc]
                tmp_bboxes = np.vstack((rcx - rcw / 2, rcy - rch / 2, rcx + rcw / 2, rcy + rch / 2))
                tmp_bboxes = np.vstack((tmp_bboxes / s, scores))
                tmp_bboxes = tmp_bboxes.transpose()
                return tmp_bboxes

            tmp_bboxes = _calc_bounding_boxes()
            bboxes = np.vstack((bboxes, tmp_bboxes))  # <class 'tuple'>: (5265, 5)

        print("time {:.2f} secs for {}".format(time.time() - start, fname))

        # non maximum suppression
        # refind_idx = util.nms(bboxes, nms_thresh)
        refind_idx = tf.image.non_max_suppression(tf.convert_to_tensor(bboxes[:, :4], dtype=tf.float32),
                                                  tf.convert_to_tensor(bboxes[:, 4], dtype=tf.float32),
                                                  max_output_size=bboxes.shape[0], iou_threshold=nms_thresh)
        refind_idx = sess.run(refind_idx)
        refined_bboxes = bboxes[refind_idx]
        return refined_bboxes


def detect_from_img_path(img_path):
    with tf.Graph().as_default():
        detections = evaluate(img_path, prob_thresh=0.5, nms_thresh=0.1,lw=3)
    return detections
