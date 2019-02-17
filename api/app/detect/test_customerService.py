# try the servicecustomer class
import camera
import customerservices as cs

# Generate a list a Camera
# Create Camera object (obtained from registration)
camera1 = camera.camera(1, 35.679221, 139.776093, "C1", "Restaurant A", "sushi")
camera2 = camera.camera(2, 35.670262, 139.775106,"C2", "Restaurant B", "sushi")
camera3 = camera.camera(3, 35.670259, 139.7751036,"C3", "Restaurant C", "sushi")
camera4 = camera.camera(4, 35.670249, 139.7751056,"C4", "Entrance A", "nightclub")

camlist =[camera1, camera2, camera3, camera4]

service = cs.customerservices()

Ctype = 'sushi'
UserPosition = [35.654697, 139.781929]
result = service.solve_request(camlist, Ctype, UserPosition)
print(result)