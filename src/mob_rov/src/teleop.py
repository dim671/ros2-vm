#!/usr/bin/env python3
import sys
import select
import termios
import tty
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

msg = """
Control Your mob_rov!
---------------------------
Use arrow keys:
   Up    : Move forward
   Down  : Move backward
   Left  : Turn left
   Right : Turn right
Press 'q' to quit.
"""

speed = 0.5   # linear speed (m/s)
turn  = 1.0   # angular speed (rad/s)

class TeleopNode(Node):
    def __init__(self):
        super().__init__('teleop_twist_keyboard')
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)

    def publish_cmd(self, linear, angular):
        twist = Twist()
        twist.linear.x = linear
        twist.angular.z = angular
        self.publisher_.publish(twist)

def get_key(settings):
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

def main():
    settings = termios.tcgetattr(sys.stdin)
    rclpy.init()
    node = TeleopNode()
    print(msg)
    try:
        while True:
            key = get_key(settings)
            if key == 'q' or key == '\x03':  # q or Ctrl-C to quit
                break
            elif key == '\x1b':  # if key is an escape sequence (arrow keys start with ESC)
                key2 = get_key(settings)
                key3 = get_key(settings)
                if key2 == '[':
                    if key3 == 'A':      # Up arrow
                        node.publish_cmd(speed, 0.0)
                    elif key3 == 'B':    # Down arrow
                        node.publish_cmd(-speed, 0.0)
                    elif key3 == 'C':    # Right arrow
                        node.publish_cmd(0.0, -turn)
                    elif key3 == 'D':    # Left arrow
                        node.publish_cmd(0.0, turn)
            else:
                # if no recognized key is pressed, send zero velocity
                node.publish_cmd(0.0, 0.0)
    except Exception as e:
        print(e)
    finally:
        node.publish_cmd(0.0, 0.0)
        rclpy.shutdown()

if __name__ == '__main__':
    main()
