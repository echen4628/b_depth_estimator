class depth_estimator:
    def __init__(self, focal_length, camera_height, camera_width, camera_pixel_height, camera_pixel_width):
        """
        focal_length: optics stuff
        camera_height: the physical height of the camera sensor
        camera_width: the physical width of the camera sensor
        camera_pixel_height: how many pixels from top to bottom
        camera_pixel_width: how many pixels from the left to the right
        bear in mind that height and width is relative to the picture. 
        if the height of the portrait is A and the width of the portrait is B, 
        then the height of the landscape is B and the width of the landscape is A
        """
        self.focal_length = focal_length
        self.camera_height = camera_height
        self.camera_width = camera_width
        self.camera_pixel_height = camera_pixel_height
        self.camera_pixel_width = camera_pixel_width
    
    def object_height(self, pixel_height):
        """
        inputs:
            pixel_height: the number of pixels the height of the object takes up
        outputs:
            object_height_on_sensor: the physical height the object takes up on the sensor
        """
        object_height_on_sensor = self.camera_height * pixel_height / self.camera_pixel_height
        return object_height_on_sensor

    def estimate(self, real_object_height,pixel_height):
        """
        inputs:
            real_object_height: the real height of the object
            pixel_height: the number of pixels the height of the object takes up
        output:
            distance: the estimated distance to the object in the same units as the real_object_height
        """
        object_height_on_sensor = self.object_height(pixel_height)
        distance = real_object_height * self.focal_length / object_height_on_sensor
        return distance
        
    
    
