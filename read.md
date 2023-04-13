# Employee Face attendance system

Is an automated system that recognizes staff that have attended for work.

# Technologies

Python, OpenCV, Pillow.<br>
Haar cascade frontal face classifier for detecting face on an image.<br>

# How to use

Admin can register a worker.<br>
Admin starts camera to capture staff photos.<br>
Admin train images.<br>
Worker presents face for attendance he/she can chek in and check out.<br>

# How training images is acheived.
Fisrt images must be capture by use of a web camera.<br>
Images are capture automatically and will be stored according to staff No.<br>
Training images is achieved by looping through employee images of each sub folder.<br>
The system recognizes the face region of interest and appended as features.<br>
The labels which are now index of each sub folder are appended as labels.<br>
The system trains features and labels and face_trained.yml is saved.<br>

# How Recogintion works
Each sub folder in employee images is stored as a list.<br>
The syteem recognizes the id based of the features.<br>
If confidence is grater than 70 the face matches.<br>
The id reads the index of list which the id belong and employee no is acquired.<br>
Based on employee no gets the employee name in the database and can check in or check out.<br>