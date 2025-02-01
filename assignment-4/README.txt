== Description ==
This is a program that allows users to both send and receive
direct messages from other users through a DSP platform. Users
can create a profile which stores general information, such as 
username, password, and server address, as well as their sent and
received messages, enabling access to chat history even without
Internet connection.

== Usage ==

GUI.py
Upon start, a user can choose to create or load a profile by selecting
File from the top menu.
 - Create Profile: File > Create Profile
   User will be prompted to enter a username, password, server address,
   and the location of their .dsu file.
 - Load Profile: File > Load Profile
   User will be prompted to open the .dsu file associated with their 
   profile.

The user can then send messages to friends they have added that are
displayed in the treeview on the left or they can add a new contact
to send a message to by selecting Settings in the top bar.
 - Add Contact: Settings > Add Contact
   User will be prompted to enter the username of the contact they wish
   to add, which will then add that contact to the treeview on the left.

The user can also edit their profile by selecting Settings in the top bar.
 - Edit Profile: Settings > Edit Profile
   User will be shown their current information (username, password,
   server) and will be given the option to edit the information.

   It is important to note that changing one's information can lead to
   complications with sending/receiving messages through the DSP platform
   as all information is referenced through their username and password. 