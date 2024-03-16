#!/usr/bin/env python3

import rospy
from nav_msgs.msg import OccupancyGrid
import numpy as np
import map_conversions as mc
import create_occ_grid as cog

def env_to_occ_grid():
    # initialize ROS node
    rospy.init_node('occ_grid_node')
    rospy.loginfo("Node is starting")

    # read map parameters
    boundary = rospy.get_param('~boundary')  # format: [xmin, ymin, xmax, ymax]
    blocks = rospy.get_param('~blocks')      # format: [[xmin, ymin, xmax, ymax], ...]
    resolution = rospy.get_param('~resolution')  # sell size
    
    # create an empty occupancyGrid message
    occ_grid_msg = OccupancyGrid()

    # fill in the header of the message
    occ_grid_msg.header.stamp = rospy.Time.now()
    occ_grid_msg.header.frame_id = 'map'

    # fill in the metadata of the message
    occ_grid_msg.info.resolution = resolution
    occ_grid_msg.info.origin.position.x = boundary[0]
    occ_grid_msg.info.origin.position.y = boundary[1]
    occ_grid_msg.info.origin.position.z = 0.0
    occ_grid_msg.info.origin.orientation.x = 0.0
    occ_grid_msg.info.origin.orientation.y = 0.0
    occ_grid_msg.info.origin.orientation.z = 0.0
    occ_grid_msg.info.origin.orientation.w = 1.0

    # create the occupancy grid using the provided boundary, blocks, and resolution
    occupancy_grid = cog.create_occupancy_grid(boundary, blocks, resolution)

    # fill in the data field of the message
    occ_grid_msg.info.width = len(occupancy_grid[0])  # Number of columns
    occ_grid_msg.info.height = len(occupancy_grid)    # Number of rows
    occ_grid_msg.data = occupancy_grid.ravel().tolist()

    # create a publisher to publish the occupancy grid message
    pub = rospy.Publisher('map', OccupancyGrid, latch=True, queue_size=1)

    # publish the message
    pub.publish(occ_grid_msg)

    rospy.loginfo("Occupancy grid published")

    # prevent the node from exiting
    rospy.spin()

if __name__ == '__main__':
    try:
        env_to_occ_grid()
    except rospy.ROSInterruptException:
        pass