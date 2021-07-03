#!/usr/bin/python3
import argparse
import cv2
import math
import numpy as np
from lsb import LSB
from error import ImageNotFoundError,DataOverflowError
from message import Message

def psnr(img1, img2):
	rms = math.sqrt(np.sum((img1.astype('float') - img2.astype('float')) ** 2) / (img1.shape[1] * img1.shape[0]))+1.5
	print("rms:{}".format(rms))
	return 20 * math.log10(256 / rms)

def create_arguments():

	parser = argparse.ArgumentParser(
		description='A LSB-based algorithm Steganography Program'
	)
	parser.add_argument("original_img", help="The original image path that you will put a hidden message")
	parser.add_argument("secret_message", help="Your secret message file path. The message must be stored inside a file.")
	parser.add_argument("number_of_chanel", help="Number of chanel use", type=float)
	parser.add_argument("-e", "--extract", help="Extract the secret message from a stegano image. \n If this option is used, <original_image> argument is treated as <stegano_image> and <secret_message> will become the stored secret message path", action="store_true")
	parser.add_argument("-o", "--output", help="Stegano Image output. The image that has a hidden message stored inside.")

	return parser.parse_args()

def extract(args):
	try:
		lsb = LSB(args.original_img,args.number_of_chanel)
	except ImageNotFoundError:
		print("Image Not Found Please Give Right File Path!!!")
		return

	binary_list = lsb.show( )
	msg = Message()
	msg.extract_msg(binary_list)
	msg.write_msg(args.secret_message)
	return

# create stegano image
def create(args):
	try:
		lsb = LSB(args.original_img,args.number_of_chanel)
	except ImageNotFoundError:
		print("Image Not Found Please Give Right File Path!!!")
		return
	orig_extension = args.original_img.split('.')[-1]


	try:
		msg = Message(pathname=args.secret_message)
	except FileNotFoundError:
		print("Message File Not Found Please Give Right File Path!!!")
		return
	binary_list = msg.create_binary_list()
	#print(bitplane_msg[:10])


	try:
		img_result = lsb.hide(binary_list)
	except DataOverflowError:
		print("All pixcel of Carrier image including {} chanel has modified no more data can be stored".format(args.number_of_chanel))
		return
		
	if args.output == None:
		args.output = 'output'
	args.output += "." + orig_extension

	cv2.imwrite(args.output, img_result)
	origin_image = cv2.imread(args.original_img, -1)
	embed_image = cv2.imread(args.output,-1)
	
	psnr_value = psnr(origin_image, embed_image)

	print("PSNR: {}".format(psnr_value))
	# show embedded & original image
	cv2.imshow('Original Image', origin_image)
	cv2.imshow("Embedded Image (PSNR: {})".format(psnr_value),embed_image)
	cv2.waitKey(0)
	return

if __name__ == '__main__':

	args = create_arguments()
	#print(args)
	#print("Original Image: {}".format(args.original_img))
	if args.extract:
		extract(args)
	else:
		create(args)
