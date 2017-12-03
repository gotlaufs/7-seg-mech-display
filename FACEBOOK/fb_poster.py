#!/usr/bin/env python3
"""Facebook 7-seg parrot poster"""

import facebook
import requests

# TODO: Add logging
# TODO: Add exception handling for every method
class FacebookPoster():
	"""Handle everything Facebook related"""
	self.POST_ID = "179361902645989"
	self.HASHTAG = "#7SAY"

	def __init__(self):
		"""Initializer"""
		pass

	def main():
		"""Main method for class"""
		# KISS mockup of class operation
		self.log_in()
		self.get_token()		# Access token for Facebook API
		self.get_post()
		self.get_comments()
		self.get_hashtags()		# Filter comments that contain Hashtag
		self.comment_in_json()	# JSON file where the comments we have replied to are stored
		self.author_following()
		self.post_reply()		
		self.post_video()

	def log_in(self):
		"""Log in to Facebook API"""
		pass

	def get_token(self):
		"""Get session token"""
		# Probably merge with log_in
		self.token = "EAACEdEose0cBACQJil85gDqiRttA7wbTn1wlS2WosKDAbKzjRBLxD8lHpxjf7WebNUZCUwPSg0tKeY23L8GOxIYSCZCnXZBWs2DIiRx1nPb1KzC8zwqs07ifXSUHeQa4Y8J50u8KHdv5BywUVCWxbvIUgZAS9UAShffXqn9VT4hY2XSNE5imVIou4RYdlOwdfIlJdSHEjQZDZD"
		self.graph = facebook.GraphAPI(self.token)

	def get_post(self):
		"""Get the Post object"""
		self.post = graph.get_object(POST_ID)

	def get_comments(self):
		"""Get the comments of the Post object"""
		self.comments = graph.get_connections(post['id'], 'comments')

	def get_hashtags(self):
		"""Get comments with Hashtag"""
		# Only first level comments should be checked for hashtag. Maybe.
		passl

	def comment_in_json(self):
		"""Check if the comment is already in the JSON "database" """
		pass

	def author_following(self):
		"""Check if comment author is following the EK Page"""
		pass

	def post_reply(self, comment):
		"""Post replay to a 'comment'"""
		pass

	def post_video(self, comment):
		"""Post a video reply to a 'comment'"""
		pass
