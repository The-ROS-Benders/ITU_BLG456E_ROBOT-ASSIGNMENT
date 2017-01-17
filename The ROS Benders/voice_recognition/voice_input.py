#!/usr/bin/env python

import rospy
from std_msgs.msg import String, Int32
from sound_play.libsoundplay import SoundClient
import time

class RobotVoice:

    def  __init__(self):

        rospy.init_node('voice_input')
        rospy.Subscriber('/recognizer/output', String, self.voice_command_callback)
 	self.pub = rospy.Publisher('/out_value', Int32, latch=True, queue_size=10)
	self.soundhandle = SoundClient()
	
	
	self.initialized = False
	self.user_gave_number = False
	self.robot_speaking = False
	self.last_time = 0
	self.welcome_message = "Hello Human, just tell me the room number and i take you there"
	self.number_array = []
	self.number_dict = {'zero': 0, 'one': 1, 'two': 2,
			    'three': 3, 'four': 4, 'five': 5,
			    'six': 6, 'seven': 7, 'eight': 8,
			    'nine': 9 }
	self.key_array = ['zero', 'one', 'two',
			    'three', 'four', 'five',
			    'six', 'seven', 'eight',
			    'nine']

        rate = rospy.Rate(1)

        rospy.loginfo("Ready to receive voice commands")
        
        while not rospy.is_shutdown():
            rate.sleep()


    def voice_command_callback(self, msg):

	difference =  time.time() - self.last_time

	if difference > 6:
	
		command = msg.data
	
		if not self.initialized:
			if command == "hello":
				print(self.welcome_message)
				self.last_time = time.time()
				self.soundhandle.say(self.welcome_message)
				self.initialized = True
		else:

			if self.user_gave_number:
			
				if command in ["yes", "no"]:
				
					self.user_gave_number = False
					num = int(''.join(str(i) for i in self.number_array))
					self.number_array = []

					if command == "yes":
						print("I am going to an adventure Hoooooooooooooooray !")
						self.last_time = time.time()
						self.pub.publish(num)
						self.soundhandle.say("I am going to an adventure Hoooooooooooooooray !")
						
					elif command == "no":
						print("Come on human, I am a robot ! Just clearly indicate your room number again.")
						self.last_time = time.time()
						self.soundhandle.say("Come on human, I am a robot ! Just clearly indicate your room number again.")
						
			elif command in self.key_array:
			
				self.number_array.append(self.number_dict[command])
				print("You said {}".format(command))

				if len(self.number_array) == 4:
					self.user_gave_number = True
					ask_question = "The room you would like to go "
					print_num = ask_question
			
					for i in range(len(self.number_array)):
						ask_question += str(self.number_array[i])
						ask_question += " "
						print_num += str(self.number_array[i])
			
					ask_question += ". Am I right, just say yes or no."
					print_num += ". Am I right, just say yes or no."
			
					print(print_num)
					self.last_time = time.time()
					self.soundhandle.say(ask_question)
				
	

if __name__=="__main__":
    try:
      RobotVoice()
      rospy.spin()
    except rospy.ROSInterruptException:
      rospy.loginfo("Voice navigation terminated.")
