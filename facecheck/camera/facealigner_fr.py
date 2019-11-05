from imutils.face_utils.facealigner import FaceAligner
from imutils.face_utils import facealigner
from imutils.face_utils.helpers import FACIAL_LANDMARKS_68_IDXS, FACIAL_LANDMARKS_5_IDXS
import numpy as np
import cv2
import dlib

try:
    import face_recognition_models
except Exception:
    print("Please install `face_recognition_models` with this command before using `face_recognition`:\n")
    print("pip install git+https://github.com/ageitgey/face_recognition_models")
    quit()

predictor_68_point_model = face_recognition_models.pose_predictor_model_location()
predictor= dlib.shape_predictor(predictor_68_point_model)


class FaceAligner_fr(FaceAligner):
	def __init__(self, predictor, desiredLeftEye=(0.35, 0.35),
		desiredFaceWidth=280, desiredFaceHeight=None):
 		super().__init__(predictor, desiredLeftEye,desiredFaceWidth, desiredFaceHeight)


	def align_fr(self, image, shape):
		# convert the landmark (x, y)-coordinates to a NumPy array
		# shape = self.predictor(gray, rect)
		# shape = shape_to_np(shape)
 
		#simple hack ;)
		if (len(shape)==68):
			# extract the left and right eye (x, y)-coordinates
			(lStart, lEnd) = FACIAL_LANDMARKS_68_IDXS["left_eye"]
			(rStart, rEnd) = FACIAL_LANDMARKS_68_IDXS["right_eye"]
			# myradio = 1.45
			# mywidthadd = 25
			myradio = 0.75
			mywidthadd = 0		# desiredFaceWidth=280
		else:
			(lStart, lEnd) = FACIAL_LANDMARKS_5_IDXS["left_eye"]
			(rStart, rEnd) = FACIAL_LANDMARKS_5_IDXS["right_eye"]
			# myradio = 1.75
			# mywidthadd = -6
			myradio = 1.2
			mywidthadd = 0   # desiredFaceWidth=270
			
		leftEyePts = shape[lStart:lEnd]
		rightEyePts = shape[rStart:rEnd]

		# compute the center of mass for each eye
		leftEyeCenter = leftEyePts.mean(axis=0).astype("int")
		rightEyeCenter = rightEyePts.mean(axis=0).astype("int")

		# compute the angle between the eye centroids
		dY = rightEyeCenter[1] - leftEyeCenter[1]
		dX = rightEyeCenter[0] - leftEyeCenter[0]
		angle = np.degrees(np.arctan2(dY, dX)) - 180

		# compute the desired right eye x-coordinate based on the
		# desired x-coordinate of the left eye
		desiredRightEyeX = 1.0 - self.desiredLeftEye[0]

		# determine the scale of the new resulting image by taking
		# the ratio of the distance between eyes in the *current*
		# image to the ratio of distance between eyes in the
		# *desired* image
		dist = np.sqrt((dX ** 2) + (dY ** 2))
		desiredDist = (desiredRightEyeX - self.desiredLeftEye[0])
		desiredDist *= self.desiredFaceWidth
		scale = desiredDist / dist

		# compute center (x, y)-coordinates (i.e., the median point)
		# between the two eyes in the input image
		eyesCenter = ((leftEyeCenter[0] + rightEyeCenter[0]) // 2,
			(leftEyeCenter[1] + rightEyeCenter[1]) // 2)

		# grab the rotation matrix for rotating and scaling the face
		M = cv2.getRotationMatrix2D(eyesCenter, angle, scale*myradio)

		# update the translation component of the matrix
		tX = self.desiredFaceWidth * 0.5
		tY = self.desiredFaceHeight * self.desiredLeftEye[1]
		M[0, 2] += (tX - eyesCenter[0])
		M[1, 2] += (tY - eyesCenter[1])

		# apply the affine transformation
		(w, h) = (self.desiredFaceWidth, self.desiredFaceHeight)
		output = cv2.warpAffine(image, M, (w+mywidthadd, h+mywidthadd),
			flags=cv2.INTER_CUBIC)

		# return the aligned face
		return output
