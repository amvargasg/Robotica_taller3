#!/usr/bin/env python3
 
#import roslib; roslib.load_manifest('rososc_tutorials')
import rospy
from std_msgs.msg import String


class PubSub(object):
    def __init__(self):
        rospy.init_node('test')
        self.accel_sub = rospy.Subscriber('robot_manipulator/color',String, self.imu_cb)
        self.fader_pub = rospy.Publisher('/test/pub', String, queue_size=10)
         
    def imu_cb(self, msg):
        newMsg = 'mensaje '+ msg.data
        coord = self.algo(newMsg)
        self.fader_pub.publish(coord)

    def algo(self, msg):
        coordenadas = ''
        if msg == 'mensaje r':
            coordenadas = '0,0'
        else:
            coordenadas = '1,1'
        return coordenadas


if __name__ == '__main__':
    try:
        a = PubSub()
        rospy.spin()
    except rospy.ROSInterruptException: pass