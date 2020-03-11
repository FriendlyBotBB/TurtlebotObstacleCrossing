import rospy
from threading import Timer
import random
from  geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
rospy.init_node('burak_bilge_node')

publisher_turtlebot = rospy.Publisher('/cmd_vel_mux/input/navi', Twist, queue_size = 1)

isDuz = True

movement = Twist()

movement.linear.x = 0.3
movement.linear.y = 0.0
movement.linear.z = 0.0
movement.angular.x = 0.0
movement.angular.y = 0.0
movement.angular.z = 0.0

def mover(data):
    global isDuz
    if(isDuz):
        for mesafe in data.ranges:
            if(mesafe < 0.6):
                isDuz = False
                movement.linear.x = 0.0
                movement.angular.z = -0.5
                t = Timer(3.0, yanaDevamEt)
                t.start()

def yanaDevamEt():
    movement.angular.z = 0.0
    movement.linear.x = 0.3
    t = Timer(2.0, tekrarDon)
    t.start()

def tekrarDon():
    movement.angular.z = 0.5
    t = Timer(3.2, devamEt)
    t.start()

def devamEt():
    global isDuz
    isDuz = True
    movement.angular.z = 0
    movement.linear.x = 0.3

if __name__ == '__main__':
    rate = rospy.Rate(10)
    rospy.Subscriber("/scan",LaserScan,mover)
    while not rospy.is_shutdown():
        publisher_turtlebot.publish(movement)
        rate.sleep()
    rospy.spin()
