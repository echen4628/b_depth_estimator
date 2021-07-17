import os
class depth_estimator:
    def __init__(self, focal_length, camera_width, camera_height, camera_pixel_width, camera_pixel_height, classes, error):
        """
        focal_length: optics stuff
        camera_height: the physical height of the camera sensor
        camera_width: the physical width of the camera sensor
        camera_pixel_height: how many pixels from top to bottom
        camera_pixel_width: how many pixels from the left to the right
        classes: a dictionary {class_number: (actual width, actual height)}
        bear in mind that height and width is relative to the picture. 
        if the height of the portrait is A and the width of the portrait is B, 
        then the height of the landscape is B and the width of the landscape is A
        error: determines how close the actual and bbox height/width ratio needs to be be to be
            considered equal
        """
        self.focal_length = focal_length
        self.camera_height = camera_height
        self.camera_width = camera_width
        self.camera_pixel_height = camera_pixel_height
        self.camera_pixel_width = camera_pixel_width
        self.classes = classes
        self.e = error
    
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
    
    def yolo2pixel(self, box):
        """
        inputs:
            box: a list describing a bbox in yolo format [class,x,y,width,height]
        outputs:
            obj_class: an int that corresponds to the object class
            obj_width: a double that represents the width of the object in pixels
            obj_height: a double that represents the height of the object in pixels
        """
        obj_class = int(box[0])
        obj_width = float(box[3])*self.camera_pixel_width
        obj_height = float(box[4])*self.camera_pixel_height
        return obj_class, obj_width, obj_height
    
    def dimension_ratio(self, obj_class, obj_width, obj_height):
        """
        inputs:
            obj_class: an int that corresponds to the object class
            obj_width: a double that represents the width of the object in pixels
            obj_height: a double that represents the height of the object in pixels
        output:
            bbox_ratio: a double that represents the ratio of the width to the height of the bounding box
            actual_ratio: a double that represents the ratio of the actual width to height of the object
        """
        bbox_ratio = obj_width/obj_height
        actual_ratio = self.classes[obj_class][0]/self.classes[obj_class][1]
        return bbox_ratio, actual_ratio

    def logic(self, bbox_ratio, actual_ratio):
        """
        probably should be renamed.
        inputs:  
            bbox_ratio: a double that represents the ratio of the width to the height of the bounding box
            actual_ratio: a double that represents the ratio of the actual width to height of the object
        outputs:
            index: 0 selects either the average, 
                    1 selects the estimation from width, 
                    2 selects the estimation from height
        """
        if actual_ratio- bbox_ratio < self.e:
            print("width and height ratio is as expect")
            return 0
        elif actual_ratio < bbox_ratio:
            print("the height is smaller than expected, the object is probably tilted around the y axis")
            return 1      
        elif actual_ratio > bbox_ratio:
            print("the width is smaller than expect, the object is probably tilted around the z axis")
            return 2


    def read_txt(self, file_path):
        """
        input:
            file_path: a string that represents the name of one file
        output:
            all_bboxes: a list of lists. All the bboxs in yolo format in a single image file
        """
        with open(file_path, "r") as bbox:
            bbox_raw = bbox.read()
            bbox_raw = bbox_raw.split()
            all_bboxes = []
            i = 0
            while i < len(bbox_raw):
                all_bboxes.append(bbox_raw[i:i+5])
                i += 5
            return all_bboxes
    
    def single_bbox_estimate(self, obj_class, obj_width, obj_height):
        """
        input:
            obj_class: an int that corresponds to the object class
            obj_width: a double that represents the width of the object in pixels
            obj_height: a double that represents the height of the object in pixels
        output:
            index: an int that selects from the distances tuple
            distances: a tuple in the form of (averaged_distance, estimated_distance_width, estimated_distance_height)
        """
        width = self.classes[obj_class][0]
        height = self.classes[obj_class][1]
        estimated_distance_width = self.estimate(width, obj_width)
        estimated_distance_height = self.estimate(height, obj_height)
        print("distance to ", self.classes[obj_class],  " estimated using width is ", estimated_distance_width)
        print("distance to ", self.classes[obj_class],  " estimated using height is ", estimated_distance_height)
        bbox_ratio, actual_ratio = self.dimension_ratio(obj_class, obj_width, obj_height)
        index = self.logic(bbox_ratio, actual_ratio)
        averaged_distance = (estimated_distance_width + estimated_distance_height)/2
        distances = (averaged_distance, estimated_distance_width, estimated_distance_height)
        return index, distances

    def single_image_estimate(self, yolo_file, output_file_path):
        """
        input:
            yolo_file: a string that represents the name of the file containing all the bboxs
            output_file_path: a string that represents the name of output file containing all the estimated distances
        output:
            nothing, just writes to the output_file_path
        """
        all_bboxes = self.read_txt(yolo_file)
        output_file = open(output_file_path, "a")
        print(file, file=output_file)
        for box in all_bboxes:
            obj_class, obj_width, obj_height = self.yolo2pixel(box)
            print("obj_class: ", obj_class, file=output_file)
            print("obj_width: ", obj_width, file=output_file)
            print("obj_height: ", obj_height, file=output_file)
            index, distances = self.single_bbox_estimate(obj_class, obj_width, obj_height)
            print(str(index) + " ", distances, file=output_file)

            
if __name__ == "__main__":
    estimator = depth_estimator(4.25, 4.2, 5.6, 3024, 4032, {0:(1.5,4), 1:(2.75,4.45), 2:(1.2,4.5)}, 0.02)
    files = os.listdir()
    files = list(filter(lambda file: file[-3:]=="txt", files))
    for file in files:
        estimator.single_image_estimate(file, "estimated_distance.txt")
    # all_bboxes = estimator.read_txt("IMG_2209.txt")
    # for box in all_bboxes:
    #     obj_class, obj_width, obj_height = estimator.yolo2pixel(box)
    #     width = estimator.classes[obj_class][0]
    #     height = estimator.classes[obj_class][1]
    #     estimated_distance_width = estimator.estimate(width, obj_width)
    #     estimated_distance_height = estimator.estimate(height, obj_height)
    #     print("distance to ", estimator.classes[obj_class],  " estimated using width is ", estimated_distance_width)
    #     print("distance to ", estimator.classes[obj_class],  " estimated using height is ", estimated_distance_height)








    # focal_length = 4.25
    # camera_height = 1
    # camera_width = 2
    # camera_pixel_height = 4032
    # camera_pixel_width = 3024
    # files = os.listdir()
    # files = list(filter(lambda file: file[-3:]=="txt", files))
    # for file in files:
    #     with open(file,"r") as bbox:
    #         a = bbox.read()
    #         a = a.split()
    #         b = []
    #         i = 0
    #         while i < len(a):
    #             b.append(a[i:i+5])
    #             i += 5
    #         print(b)
    #         for box in b:
    #             print(box)
    #             obj_class = box[0]
    #             obj_width = float(box[3])
    #             obj_height = float(box[4])
    #             print(obj_class)
    #             print(obj_width*camera_pixel_width)
    #             print(obj_height*camera_pixel_height)

                