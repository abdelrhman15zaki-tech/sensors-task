#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
import math
import time
from sensor_msgs.msg import LaserScan
class Publisher(Node):
    def __init__(self):
        super().__init__('fake_lidar')
        self.get_logger().info('This is FAKE Lidar data')# this is what prints in the terminal
        self.start_time=time.monotonic()
        self.publisher=self.create_publisher(LaserScan,'/scan',10)
        self.timer=self.create_timer(.1,self.generate_fake_lidar)
    def generate_fake_lidar(self):
        fake=LaserScan()
        fake.scan_time=0.1 # f= 10hz , T=1/f=0.1 sec
        #min & max angles
        fake.angle_min=-1.0*math.pi
        fake.angle_max=1.0*math.pi

        fake.angle_increment=1.0*math.pi/180.0 # the angle is in radian, to convert from degrees to radian multipy by PI/180
        
        fake.range_min=0.1 # its uint is meter
        fake.range_max=15.0

        fake.header.frame_id="lidar_position"
        fake.header.stamp=self.get_clock().now().to_msg()
        #for making the obstacles moving
        t=time.monotonic()-self.start_time
        ranges=[5.0]*360# the angle increment is 1 degree so thats 360 indecies for the range array
        for i in range (25,76):
            ranges[i]=2.0+t*0.1
        for i in range (210,245):
            ranges[i]=0.7+math.sin(.5*math.pi*t)*2
        for i in range (112,178):
            ranges[i]=13.0-t*0.25
        for i in range (305,332):            
            ranges[i]=3.0 
        fake.intensities=[100.0]*360     
        fake.ranges=ranges
        self.publisher.publish(fake)      
def main(args=None):
    rclpy.init(args=args)
    node = Publisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
