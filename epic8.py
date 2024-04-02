import sys
import datetime
import os


# Class for a user account
class UserAccount:
  in_college_app = None

  def __init__(
      self,
      username,
      password,
      first_name,
      last_name,
      membership_type="Standard",  # New attribute for membership type
      university=None,
      major=None,
      language="English",
      email="email_on",
      SMS="SMS_on",
      targeted_advertising_features="ads_on",
      friends=None):
    self.username = username
    self.password = password
    self.first_name = first_name
    self.last_name = last_name
    self.membership_type = membership_type  # Standard or Plus
    self.university = university
    self.major = major
    self.language = language
    self.email = email
    self.SMS = SMS
    self.targeted_advertising_features = targeted_advertising_features
    self.friends = []  # New attribute for friends list
    self.pending_friend_requests = []
    self.profile = None
    self.inbox = []  # New attribute for inbox

  @classmethod
  def set_in_college_app(cls, in_college_app_instance):
    cls.in_college_app = in_college_app_instance

  def view_inbox(self):
    if not self.inbox:
      print("Your inbox is empty.")
      return
    print("Your inbox:")
    for idx, message in enumerate(self.inbox, start=1):
      status = "Read" if message.get("read", False) else "Unread"
      print(
          f"{idx}. From: {message['sender']} - {status} - {message['content']}"
      )

    while True:
      print("\nChoose from the menu below:")
      print("1. Read a message")
      print("2. Back to Main Menu")
      choice = input("\nEnter your choice: ")

      if choice == '1':
        message_index = int(
            input("Enter the number of the message you want to read: "))
        self.view_message(message_index)
      elif choice == '2':
        break
      else:
        print("Invalid choice. Please try again.")

  def view_message(self, message_index):
    if message_index < 1 or message_index > len(self.inbox):
      print("Invalid message number.")
      return

    message = self.inbox[message_index - 1]
    print(f"\nFrom: {message['sender']}\nMessage: {message['content']}")
    message["read"] = True  # Mark as read

    while True:
      print("\nChoose from the menu below:")
      print("1. Respond")
      print("2. Delete")
      print("3. Back to Inbox")
      action = input("\nEnter your choice: ")

      if action == "1":
        response_message = input("Type your response: ")
        self.respond_to_message(message_index, response_message)
      elif action == "2":
        self.inbox.pop(message_index - 1)
        print("Message deleted.")
        break
      elif action == "3":
        break
      else:
        print("Invalid choice. Please try again.")

  # Method to send an initial message
  def send_initial_message(self, recipient_username, message_content):
    recipient = self.in_college_app.accts.get(recipient_username)
    if not recipient:
      print(f"User '{recipient_username}' not found.")
      return

    # Allow Plus users to send messages to anyone, Standard users can only send to friends
    if self.membership_type != "Plus" and recipient_username not in self.friends:
      print("I'm sorry, you are not friends with that person.")
      return

    # Write the message to the messages_inbox.txt file
    with open("messages_inbox.txt", "a") as file:
      file.write(
          f"{self.username}:{recipient_username}:{message_content}:{self.membership_type == 'Plus'}:False\n"
      )

    # Update the recipient's inbox in the application
    recipient.inbox.append({
        "sender": self.username,
        "recipient": recipient_username,
        "content": message_content,
        "original_sender_plus": self.membership_type == "Plus",
        "read": False
    })
    print(f"Message sent to {recipient_username}.")

  # Method to respond to a message
  def respond_to_message(self, message_index, response_message):
    if message_index < 1 or message_index > len(self.inbox):
      print("Invalid message number.")
      return

    message = self.inbox[message_index - 1]
    original_sender = self.in_college_app.accts.get(message['sender'])
    if original_sender:
      # Check if the original sender is a Plus member or if they are friends
      if message.get("original_sender_plus",
                     False) or message['sender'] in self.friends:
        # Write the response message to the original sender's inbox in the file
        with open("messages_inbox.txt", "a") as file:
          file.write(
              f"{self.username}:{message['sender']}:{response_message}:{self.membership_type == 'Plus'}:False\n"
          )

        # Update the original sender's inbox in the application
        original_sender.inbox.append({
            "sender":
            self.username,
            "recipient":
            message['sender'],
            "content":
            response_message,
            "original_sender_plus":
            self.membership_type == "Plus",
            "read":
            False
        })
        print("Response sent.")
      else:
        print("You cannot respond to this message.")
    else:
      print(f"User '{message['sender']}' not found.")

  def create_experience(self):
    experiences = []
    for _ in range(3):
      job_title = input("Enter job title (or leave blank to finish): ")
      if not job_title:
        break
      employer = input("Enter employer: ")
      start_date = input("Enter start date (MM/YYYY): ")
      end_date = input("Enter end date (MM/YYYY): ")
      location = input("Enter location: ")
      description = input("Enter description of what you did: ")
      experience = {
          "title": job_title,
          "employer": employer,
          "start_date": start_date,
          "end_date": end_date,
          "location": location,
          "description": description
      }
      experiences.append(experience)
    return experiences

  def create_education(self):
    educations = []
    while True:
      school_name = input("Enter school name (or leave blank to finish): ")
      if not school_name:
        break
      degree = input("Enter degree: ")
      years_attended = input("Enter years attended (YYYY-YYYY): ")
      education_info = {
          "school_name": school_name,
          "degree": degree,
          "years_attended": years_attended
      }
      educations.append(education_info)
    return educations

#ADD VALIDATION

  def create_profile(self):

    #one line of text
    title = input("Enter profile title: ")

    #convert, words must start with uppercase
    major = input("Enter major: ").capitalize()

    #words must start with uppercase
    university = input("Enter university name: ").capitalize()

    about = input("Enter about information: ")

    #up to 3 past jobs
    experiences = self.create_experience()
    education = self.create_education()

    self.profile = Profile(title, major, university, about, experiences,
                           education)

  def update_profile(self):
    if self.profile:
      print("Current profile:")
      self.profile.display_profile(f"{self.first_name} {self.last_name}")
      update_choice = input(
          "What do you want to update? (title/major/university/about/experience/education): "
      )
      if update_choice.lower() == 'title':
        self.profile.title = input("Enter new title: ")
      elif update_choice.lower() == 'major':
        self.profile.major = input("Enter new major: ").capitalize()
      elif update_choice.lower() == 'university':
        self.profile.university = input(
            "Enter new university name: ").capitalize()
      elif update_choice.lower() == 'about':
        self.profile.about = input("Enter new about information: ")
      elif update_choice.lower() == 'experience':
        self.profile.experience = self.create_experience()
      elif update_choice.lower() == 'education':
        self.profile.education = self.create_education()
    else:
      self.create_profile()

  def view_profile(self, profile_owner_username=None):
    if profile_owner_username:
      profile_owner = self.in_college_app.accts.get(profile_owner_username)
      if profile_owner and profile_owner.profile:
        profile_owner.profile.display_profile(
            f"{profile_owner.first_name} {profile_owner.last_name}")
      else:
        print("Profile not available.")
    else:
      if self.profile:
        self.profile.display_profile(f"{self.first_name} {self.last_name}")
      else:
        print("Profile not available.")


# Class for job posting
class Job:

  def __init__(self, title, description, employer, location, salary, poster):
    self.title = title
    self.description = description
    self.employer = employer
    self.location = location
    self.salary = salary
    self.poster = poster


class Profile:

  def __init__(self,
               title,
               major,
               university,
               about,
               experience=None,
               education=None):
    self.title = title
    self.major = major
    self.university = university
    self.about = about
    self.experience = experience if experience is not None else []
    self.education = education if education is not None else []

  def display_profile(self, student_name):
    print(f"Profile of {student_name}:")
    print(f"Title: {self.title}")
    print(f"Major: {self.major}")
    print(f"University: {self.university}")
    print(f"About: {self.about}")
    print("Experience:")
    for exp in self.experience:
      print("- Title:", exp.get('title'))
      print("  Employer:", exp.get('employer'))
      print("  Date Started:", exp.get('start_date'))
      print("  Date Ended:", exp.get('end_date'))
      print("  Location:", exp.get('location'))
      print("  Description:", exp.get('description'))
    print("Education:")
    for edu in self.education:
      print("- School Name:", edu.get('school_name'))
      print("  Degree:", edu.get('degree'))
      print("  Years Attended:", edu.get('years_attended'))


class MenuOptionCommand:

  def __init__(self, app):
    self.app = app

  def execute(self):
    raise NotImplementedError


class JobCommand(MenuOptionCommand):

  def execute(self):
    applied_jobs = self.app.applied_jobs_list(self.app.loggedInAcct.username)
    print(f"\nYou have currently applied for {len(applied_jobs)} job(s).")
    while True:

      #Notification for if jobs applied for are deleted

      # Read job_applications.txt file
      with open('job_applications.txt', 'r') as file:
        lines = file.readlines()

      # Check for JOBDELETED:(your username)
      modified_lines = []
      job_deleted_notification = False
      for line in lines:
        if line.strip() == f"JOBDELETED:{self.app.loggedInAcct.username}":
          print("**Previous Job(s) you applied for have been deleted**")
          job_deleted_notification = True
        else:
          modified_lines.append(line)

      # Rewrite the file with updated content
      if job_deleted_notification:
        with open('job_applications.txt', 'w') as file:
          file.writelines(modified_lines)

      print("\nChoose from the menu below:")
      print("1. Search for Jobs")
      print("2. See applied jobs")
      print("3. See unapplied jobs")
      print("4. See saved jobs")
      print("5. Back to Main Menu")
      option = input("\nEnter your choice: ")
      if option == '5':
        break
      elif option == '1':
        self.app.searchForAJob()
      elif option == '2':
        self.app.print_applied_jobs(self.app.loggedInAcct.username)
      elif option == '3':
        self.app.print_unapplied_jobs(self.app.loggedInAcct.username)
      elif option == '4':
        self.app.print_saved_jobs(self.app.loggedInAcct.username)


class FindPeopleMenuCommand(MenuOptionCommand):

  def execute(self):
    self.app.findPeopleMenu()


class SkillsMenuCommand(MenuOptionCommand):

  def execute(self):
    self.app.skillsMenu()


class AddJobPostCommand(MenuOptionCommand):

  def execute(self):
    self.app.addJobPost()


class DeleteJobPostCommand(MenuOptionCommand):

  def execute(self):
    self.app.deleteJobPost()


class ApplyForJobCommand(MenuOptionCommand):

  def execute(self):
    self.app.applyForJob()


class ViewPendingRequestsCommand(MenuOptionCommand):

  def execute(self):
    self.app.view_pending_friend_requests()


class ShowFriendsListCommand(MenuOptionCommand):

  def execute(self):
    self.app.show_friends_list()


class EditProfileCommand(MenuOptionCommand):

  def execute(self):
    self.app.edit_profile()


class ViewProfileCommand(MenuOptionCommand):

  def execute(self):
    if not self.app.loggedInAcct:
      print("Please log in first.")
      return

    # Display logged-in user's profile
    print("Your Profile:")
    self.app.loggedInAcct.view_profile()

    # Display menu with friend profiles
    print("\nFriends List:")
    self.app.show_friends_list_profiles()


# Class for app accounts
class InCollegeAccts:
  MAX_ACCOUNTS = 10
  MAX_JOBS = 10

  def __init__(self):
    self.accts = {}
    self.jobs = []
    self.applications = []
    self.jobsSaved = []
    self.loggedInAcct = None
    self.loadAccts()
    self.loadJobPosts()
    self.loadProfiles()
    self.loadJobApplications()
    self.loadJobsSaved()
    self.ensure_messages_inbox_file_exists()

  def displayNewNotifications(self, username):
    try:
        # Load seen notifications
        with open(f"{username}_notifications.txt", "r") as file:
            seen_notifications = file.read().splitlines()
    except FileNotFoundError:
        seen_notifications = []

    # Load all notifications
    all_notifications = []
    try:
        with open("notifications.txt", "r") as file:
            all_notifications = file.read().splitlines()
    except FileNotFoundError:
        # If there are no general notifications, nothing to do
        return

    # Determine new notifications
    new_notifications = [note for note in all_notifications if note not in seen_notifications]

    # Display new notifications
    for notification in new_notifications:
        print(f"Notification: {notification}")  # Display the new notification

    # Update the seen notifications file
    with open(f"{username}_notifications.txt", "w") as file:
        for notification in all_notifications:
            file.write(notification + "\n")

    # If there were new notifications, update the general notifications file
    if new_notifications:
        # Overwrite the general notifications with only those not seen by anyone
        with open("notifications.txt", "w") as file:
            unseen_notifications = [note for note in all_notifications if note not in new_notifications]
            for notification in unseen_notifications:
                file.write(notification + "\n")

  def displayJobDeletionNotifications(self, username):
    # Open job_applications.txt and check for deleted jobs
    with open('job_applications.txt', 'r') as file:
        for line in file.readlines():
            if f"JOBDELETED[" in line and username in line:
                deleted_job_title = line.split("JOBDELETED[")[1].split("]")[0]
                print(f"A job you applied for, {deleted_job_title}, has been deleted.")

  def displayNewMemberNotifications(self, username):
    with open("new_users_notifications.txt", "r") as file:
        notifications = file.readlines()
    with open("new_users_notifications.txt", "w") as file:
        for notification in notifications:
            notif_user, notif_name = notification.strip().split(":", 1)
            # Skip notifying about the user themselves
            if notif_user != username:
                print(f"{notif_name} has joined InCollege.")
            else:
                # Re-add the notification for other users to see
                file.write(notification)

  def ensure_messages_inbox_file_exists(self):
    try:
      # Attempt to open the file in read mode, which will fail if the file does not exist
      with open("messages_inbox.txt", "r") as file:
        pass
    except FileNotFoundError:
      # If the file does not exist, create it by opening it in write mode
      with open("messages_inbox.txt", "w") as file:
        pass

  # New methods for friend requests and network functionality
  def send_friend_request(self, from_user, to_user):
    if from_user == to_user:
      print("You cannot add yourself as a friend.")
      return

    if to_user in self.accts and from_user in self.accts:
      if from_user not in self.accts[to_user].pending_friend_requests:
        self.accts[to_user].pending_friend_requests.append(from_user)
        print(f"Friend request sent from {from_user} to {to_user}")
        self.saveAccts()  # Make sure this line exists to save changes
      else:
        print(f"{from_user} has already sent a friend request to {to_user}.")
    else:
      print("One of the users does not exist.")

  def accept_friend_request(self, user, friend):
    if friend in self.accts[user].pending_friend_requests:
      self.accts[user].friends.append(friend)
      self.accts[friend].friends.append(user)
      self.accts[user].pending_friend_requests.remove(friend)
      print(f"{user} and {friend} are now friends")

  def remove_friend(self, user, friend):
    if friend in self.accts[user].friends:
      self.accts[user].friends.remove(friend)
      self.accts[friend].friends.remove(user)
      print(f"{user} and {friend} are no longer friends")

  def show_network(self, user):
    print("Your network:")
    for friend in self.accts[user].friends:
      print(friend)

  def view_pending_friend_requests(self):
    if not self.loggedInAcct:
      print("Please log in to view pending friend requests.")
      return
    if not self.loggedInAcct.pending_friend_requests:
      print("You have no pending friend requests.")
      return

    print("Pending friend requests:")
    for request in list(
        self.loggedInAcct.pending_friend_requests
    ):  # Copy the list to avoid modification issues during iteration
      response = input(
          f"Do you want to accept the friend request from {request}? (yes/no): "
      )
      if response.lower() == 'yes':
        self.accept_friend_request(self.loggedInAcct.username, request)
      elif response.lower() == 'no':
        self.reject_friend_request(self.loggedInAcct.username, request)
    self.saveAccts()  # Save changes after processing requests

  def reject_friend_request(self, user, friend):
    if friend in self.accts[user].pending_friend_requests:
      self.accts[user].pending_friend_requests.remove(friend)
      print(f"{user} rejected the friend request from {friend}.")
      self.saveAccts()  # Save the updated accounts

  def show_friends_list(self):
    if not self.loggedInAcct:
      print("Please log in to view your friends list.")
      return
    if not self.loggedInAcct.friends:
      print("You currently have no friends added.")
      return
    print("Your friends list:")
    for idx, friend_username in enumerate(self.loggedInAcct.friends, start=1):
      friend = self.accts.get(friend_username, None)
      if friend:
        print(
            f"{idx}. {friend.first_name} {friend.last_name} ({friend.username})"
        )
      else:
        print(f"{idx}. {friend_username} (Account not found)")

    # New functionality to remove a friend
    remove_choice = input(
        "\nDo you want to remove a friend from your list? (yes/no): ").lower()
    if remove_choice == 'yes':
      remove_idx = input("Enter the number of the friend you want to remove: ")
      try:
        remove_idx = int(remove_idx) - 1  # Adjust for zero-based indexing
        if 0 <= remove_idx < len(self.loggedInAcct.friends):
          removed_friend_username = self.loggedInAcct.friends.pop(remove_idx)
          if removed_friend_username in self.accts:
            # Remove current user from the removed friend's list
            self.accts[removed_friend_username].friends.remove(
                self.loggedInAcct.username)
            print(
                f"{removed_friend_username} has been removed from your friends list."
            )
            self.saveAccts(
            )  # Save changes if you have a method to update account data persistently
          else:
            print("Account not found. No changes made.")
        else:
          print("Invalid number. No friends removed.")
      except ValueError:
        print("Invalid input. Please enter a number.")

  def show_friends_list_profiles(self):
    if not self.loggedInAcct:
      print("Please log in to view your friends list.")
      return
    if not self.loggedInAcct.friends:
      print("You currently have no friends added.")
      return
    print("Your friends list:")
    friendslist = []
    for idx, friend_username in enumerate(self.loggedInAcct.friends, start=1):
      friend = self.accts.get(friend_username, None)
      friendslist.append(friend)
      if friend and friend.profile:
        print(
            f"{idx}. {friend.first_name} {friend.last_name} ({friend.username}) PROFILE"
        )
      elif friend:
        print(
            f"{idx}. {friend.first_name} {friend.last_name} ({friend.username})"
        )
      else:
        print(f"{idx}. {friend_username} (Account not found)")

    # Select a friend to view their profile
    if self.loggedInAcct.friends:
      friend_choice = input(
          "\nEnter the number of the friend whose profile you want to view (or '0' to go back): "
      )
      try:
        friend_choice = int(friend_choice)
        if 0 < friend_choice <= len(self.loggedInAcct.friends):
          friend_username = self.loggedInAcct.friends[
              friend_choice - 1]  # Get the friend's username
          friend_profile_owner = self.accts.get(
              friend_username)  # Retrieve the UserAccount object
          friend_profile_owner.view_profile()  # Call the view_profile method
        elif friend_choice == 0:
          return
        else:
          print("Invalid choice.")
      except ValueError:
        print("Invalid input. Please enter a number.")

  # Function to save new accounts to text file
  def saveAccts(self):
    with open("accounts.txt", "w") as file:
      for username, account in self.accts.items():
        file.write(
            f"{username}:{account.password}:{account.first_name}:{account.last_name}:{account.university}:{account.major}:{account.language}:{account.email}:{account.SMS}:{account.targeted_advertising_features}:{','.join(account.friends)}\n"
        )

  def loadAccts(self):
    try:
      with open("accounts.txt", "r") as file:
        for line in file:
          parts = line.strip().split(":")
          if len(parts) == 12:
            username, password, first_name, last_name, university, major, language, email, SMS, targeted_advertising_features, friends, membership_type = parts
          elif len(parts) == 11:
            username, password, first_name, last_name, university, major, language, email, SMS, targeted_advertising_features, friends = parts
            membership_type = "Standard"  # Default to Standard membership if not specified
          else:
            continue  # Skip lines with an incorrect number of values

          self.accts[username] = UserAccount(
              username,
              password,
              first_name,
              last_name,
              membership_type=membership_type,
              university=university,
              major=major,
              language=language,
              email=email,
              SMS=SMS,
              targeted_advertising_features=targeted_advertising_features,
              friends=friends.split(','))
    except FileNotFoundError:
      pass

  def saveProfiles(self):
    with open("profiles.txt", "w") as file:
      for username, account in self.accts.items():
        if account.profile:
          experience_str_list = []
          for exp in account.profile.experience:
            exp_str = ";".join(str(value) for value in exp.values())
            experience_str_list.append(exp_str)
          experience_str = "[" + "|".join(experience_str_list) + "]"

          education_str_list = []
          for edu in account.profile.education:
            edu_str = ";".join(str(value) for value in edu.values())
            education_str_list.append(edu_str)
          education_str = "[" + "|".join(education_str_list) + "]"

          profile_data = f"{username}:{account.profile.title}:{account.profile.major}:" \
                         f"{account.profile.university}:{account.profile.about}:" \
                         f"{experience_str}:{education_str}\n"
          file.write(profile_data)

  def loadProfiles(self):
    try:
      with open("profiles.txt", "r") as file:
        for line in file:
          parts = line.strip().split(":")
          username = parts[0]
          title = parts[1]
          major = parts[2]
          university = parts[3]
          about = parts[4]
          exp_str = parts[5]
          edu_str = parts[6]

          # Parse experience string
          experience = []
          if exp_str.strip():
            experience_data = exp_str.strip("[]").split("|")
            for exp_data in experience_data:
              exp_values = exp_data.split(";")
              if len(exp_values) == 6:  # Ensure all fields are present
                exp_dict = {
                    "title": exp_values[0],
                    "employer": exp_values[1],
                    "start_date": exp_values[2],
                    "end_date": exp_values[3],
                    "location": exp_values[4],
                    "description": exp_values[5]
                }
                experience.append(exp_dict)

          # Parse education string
          education = []
          if edu_str.strip():
            education_data = edu_str.strip("[]").split("|")
            for edu_data in education_data:
              edu_values = edu_data.split(";")
              if len(edu_values) == 3:  # Ensure all fields are present
                edu_dict = {
                    "school_name": edu_values[0],
                    "degree": edu_values[1],
                    "years_attended": edu_values[2]
                }
                education.append(edu_dict)

          # Create profile object and assign to account
          if username in self.accts:
            self.accts[username].profile = Profile(title, major, university,
                                                   about, experience,
                                                   education)
    except FileNotFoundError:
      pass

  # Function to save new job postings to text file
  def saveJobPosts(self):
    with open("jobs.txt", "w") as file:
      for job in self.jobs:
        file.write(
            f"{job.title}:{job.description}:{job.employer}:{job.location}:{job.salary}:{job.poster}\n"
        )

  #Epic 6- Function to save job applications to text file
  def saveJobApplications(self):
    with open("job_applications.txt", "w") as file:
      for job in self.applications:
        file.write(
            f"{job['job_title']}:{job['graduation_date']}:{job['start_date']}:{job['explanation']}:{job['username']}\n"
        )
    print("Job applications saved successfully!")

  #Load job applications
  def loadJobApplications(self):
    try:
      with open("job_applications.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
          job_info = line.strip().split(":")
          if len(job_info) == 5:
            job_application = {
                "job_title": job_info[0],
                "graduation_date": job_info[1],
                "start_date": job_info[2],
                "explanation": job_info[3],
                "username": job_info[4]
            }
            self.applications.append(job_application)
      print("Job applications loaded successfully!")
    except FileNotFoundError:
      print("No job applications found!")

  def saveJobsSaved(self):
    with open("job_saved.txt", "w") as file:
      for jobSaved in self.jobsSaved:
        file.write(f"{jobSaved['job_title']}:{jobSaved['username']}\n")
    print("Job saved successfully!")

  #Unmark jobs from saved
  def unmarkSavedJob(self, job_title):
    try:
      with open("job_saved.txt", "r") as file:
        lines = file.readlines()
      with open("job_saved.txt", "w") as file:
        for line in lines:
          job_info = line.strip().split(":")
          if job_info[0] == job_title:
            continue  # Skip this line if it matches the job title
          file.write(line)
      print("Job successfully unmarked!")
      self.jobsSaved = [
          job for job in self.jobsSaved if job['job_title'] != job_title
      ]

    except FileNotFoundError:
      print("No saved jobs found!")

  #load the jobs from jobs_saved.txt
  def loadJobsSaved(self):
    try:
      with open("job_saved.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
          job_info = line.strip().split(":")
          saved_job = {"job_title": job_info[0], "username": job_info[1]}
          self.jobsSaved.append(saved_job)
      print("Saved jobs loaded successfully!")
    except FileNotFoundError:
      print("No saved jobs found!")

  # Function to retrieve job posting
  def loadJobPosts(self):
    try:
      with open("jobs.txt", "r") as file:
        for line in file:
          parts = line.strip().split(":")
          if len(parts) == 6:  # Ensure that there are exactly 6 parts
            title, description, employer, location, salary, poster = parts
            self.jobs.append(
                Job(title, description, employer, location, salary, poster))
          else:
            # Handle the error: log it, raise a more descriptive error, or skip the line
            print(f"Skipping line in jobs.txt: {line.strip()}")
    except FileNotFoundError:
      print("The jobs.txt file does not exist. No jobs loaded.")

  # Function to make a new account
  def createAcct(self, username, password, first_name, last_name):
    if len(self.accts) >= self.MAX_ACCOUNTS:
      print(
          "All permitted accounts have been created, please come back later.")
      return
    # Must be a unique account
    if username in self.accts:
      print("Username already exists. Please choose a different username.")
      return
    # Password criteria
    if len(password) < 8 or len(password) > 12 or \
            not any(char.isdigit() for char in password) or \
            not any(char.isupper() for char in password) or \
            not any(char in '!@#$%^&*()_+-=[]{}|;:,.<>?~' for char in password):
      print(
          "Password must be 8-12 characters long and contain at least one uppercase letter, one digit, and one special character."
      )
      return

    # Prompt for membership type
    print("Select membership type:\n1. Standard (Free)\n2. Plus ($10/month)")
    membership_choice = input("Enter your choice (1 or 2): ")
    membership_type = "Plus" if membership_choice == "2" else "Standard"
    self.accts[username] = UserAccount(username,
                                       password,
                                       first_name,
                                       last_name,
                                       membership_type=membership_type)
    self.saveAccts()
    print("\nAccount created successfully!")
    with open("new_users_notifications.txt", "a") as file:
      new_user_notification = f"{username}:{first_name} {last_name}\n"
      file.write(new_user_notification)

  # Function to log into App
  def logIn(self, username, password):
    if username in self.accts and self.accts[username].password == password:
      self.loggedInAcct = self.accts[username]
      print("\nYou have successfully logged in")

      self.displayNewNotifications(username)
      self.displayJobDeletionNotifications(username)
      self.displayNewMemberNotifications(username)
      # Load the user's inbox from the file
      self.loadUserInbox(username)

      # Display a notification about the number of messages
      num_messages = len(self.loggedInAcct.inbox)
      print(f"You have {num_messages} message(s) waiting for y.")

      # Check for last application date
      last_application_date = None
      for application in self.applications:
        if application['username'] == username:
          application_date = datetime.datetime.strptime(
              application['graduation_date'], "%m/%d/%Y")
          if last_application_date is None or application_date > last_application_date:
            last_application_date = application_date

      if last_application_date is not None:
        days_since_last_application = (datetime.datetime.now() -
                                       last_application_date).days
        if days_since_last_application > 7:
          print(
              "Remember – you're going to want to have a job when you graduate. Make sure that you start to apply for jobs today! \n"
          )
      else:
        print(
            "Remember – you're going to want to have a job when you graduate. Make sure that you start to apply for jobs today! \n"
        )

      # Check if the user has created a profile
      if self.loggedInAcct.profile is None:
        print("Don't forget to create a profile \n")

      # Check for pending friend requests
      num_pending_requests = len(self.loggedInAcct.pending_friend_requests)
      if num_pending_requests > 0:
        print(f"You have {num_pending_requests} pending friend request(s).")
      return
    else:
      print("Incorrect username/password, please try again")

  def loadUserInbox(self, username):
    try:
      with open("messages_inbox.txt", "r") as file:
        messages = []
        for line in file:
          parts = line.strip().split(":")
          if len(parts) == 5:
            sender, recipient, content, original_sender_plus, read = parts
            if recipient == username:  # Filter messages for the logged-in user
              messages.append({
                  "sender": sender,
                  "content": content,
                  "original_sender_plus": original_sender_plus == "True",
                  "read": read == "True"
              })
        self.accts[username].inbox = messages
    except FileNotFoundError:
      pass

  # Function to display Main Menu
  def showOptionsMenu(self):
    if not self.loggedInAcct:
      print("Please log in first.")
      return
    option_commands = {
        '1': JobCommand(self),
        '2': FindPeopleMenuCommand(self),
        '3': SkillsMenuCommand(self),
        '4': AddJobPostCommand(self),
        '7': ViewPendingRequestsCommand(self),
        '8': ShowFriendsListCommand(self),
        '9': EditProfileCommand(self),
        '10': ViewProfileCommand(self),
        '11': DeleteJobPostCommand(self),
    }
    while True:
      print("\nChoose from the menu below:")
      print("1. Job search/internship")
      print("2. Find someone you know")
      print("3. Learn a new skill")
      print("4. Post a job")
      print("5. Useful Links")
      print("6. Incollege Important Links")
      print("7. View pending friend requests")
      print("8. Show my network")
      print("9. Create/Edit Profile")
      print("10. View Profiles")
      print("11. Delete a job listing")
      print("12. View Inbox")
      print("13. Back to Main Menu")
      option = input("\nEnter your choice: ")
      if option == '13':
        break
      elif option == '12':
        if self.loggedInAcct:  # Check if a user is logged in
          self.loggedInAcct.view_inbox(
          )  # Call view_inbox on the logged-in user account
        else:
          print("Please log in first.")
      elif option == '5':
        self.useful_links_menu()
      elif option == '6':
        self.important_links_menu()
      else:
        command = option_commands.get(option)
        if command:
          command.execute()
        else:
          print("Invalid choice. Please try again.")

  def edit_profile(self):
    if not self.loggedInAcct:
      print("Please log in first.")
      return
    self.loggedInAcct.update_profile()

  # Function to find others
  def findPeopleMenu(self):
    if not self.loggedInAcct:
      print("Please log in first.")
      return
    print("Search by:\n1. Last Name\n2. University\n3. Major")
    choice = input("Choose your search method (1-3): ")

    if choice not in ['1', '2', '3']:
      print("Invalid choice. Please select 1, 2, or 3.")
      return

    search_query = input("Enter your search query: ")
    found_users = []

    for account in self.accts.values():
      if choice == '1' and account.last_name.lower() == search_query.lower():
        found_users.append(account)
      elif choice == '2' and hasattr(
          account,
          'university') and account.university.lower() == search_query.lower():
        found_users.append(account)
      elif choice == '3' and hasattr(
          account, 'major') and account.major.lower() == search_query.lower():
        found_users.append(account)

    if not found_users:
      print("No users found with the provided information.")
      return

    for user in found_users:
      print(
          f"Found user: {user.first_name} {user.last_name} ({user.username})")
      action = input(
          "1. Send friend request\n2. Send message\nEnter your choice: ")
      if action == "1":
        if user.username == self.loggedInAcct.username:
          print("You cannot send a friend request to yourself.")
        elif self.loggedInAcct.username in user.pending_friend_requests:
          print("You have already sent a friend request to this user.")
        else:
          user.pending_friend_requests.append(self.loggedInAcct.username)
          print(f"Friend request sent to {user.username}.")
      elif action == "2":
        message_content = input("Enter your message: ")
        if isinstance(self.loggedInAcct, UserAccount):
          self.loggedInAcct.send_initial_message(
              user.username, message_content)  # Pass the recipient's username
        else:
          print("No user is currently logged in.")

  #New Epic 6 Function- Search for a job
  def searchForAJob(self):

    applied_jobs = self.applied_jobs_list(self.loggedInAcct.username)
    print("\nJob Titles:")
    for job in self.jobs:
      if job.title in applied_jobs:
        print(f"{job.title} [Applied]")
      else:
        print(job.title)

    title = input("\nEnter the title of the job you want to know more about: ")
    found = False
    for job in self.jobs:
      if job.title == title:
        found = True
        print("\n")
        print(f"Title: {job.title}")
        print(f"Description: {job.description}")
        print(f"Employer: {job.employer}")
        print(f"Location: {job.location}")
        print(f"Salary: {job.salary}")

        print(
            "\nChoose from the menu below:\n1. Apply\n2. Save\n3. Return to previous menu"
        )
        applyAnswer = input("\nEnter your choice: ")
        if applyAnswer == '1':
          for job_application in self.applications:
            if job_application['job_title'] == title and job_application[
                'username'] == self.loggedInAcct.username and applyAnswer.lower(
                ) == "yes":
              print("You have already applied for this job.")
              return  # Exit the function since the user cannot apply again

          if job.poster == self.loggedInAcct.username:
            print("\nYou cannot apply for your own job.")
          else:
            self.applyForJob(job)
            print("\nApplied. Returning to main menu.")
            return

          if not found:
            print(f"\nJob with title '{title}' not found.")
          print("\nReturning to main menu.")

        elif applyAnswer == '2':
          for jobSaved in self.jobsSaved:
            if jobSaved['job_title'] == title and jobSaved[
                'username'] == self.loggedInAcct.username:
              print("You have already saved for this job.")
              return  # Exit the function since the user cannot apply again

          if job.poster == self.loggedInAcct.username:
            print("\nYou cannot save your own job.")
          else:
            self.saveAJob(job)
            print("\nSaved. Returning to main menu.")
            return

          if not found:
            print(f"\nJob with title '{title}' not found.")
          print("\nReturning to main menu.")

        elif applyAnswer == '3':
          print("Returning to previous menu...")
          return

  # Function to generate a list of jobs the user applied for
  def applied_jobs_list(self, username):
    applied_jobs = []
    for job_application in self.applications:
      if job_application['username'] == username:
        applied_jobs.append(job_application['job_title'])
    return applied_jobs

  # Function to read jobs.txt and display jobs the user didn't apply for
  def unapplied_jobs_list(self, username):
    unapplied_jobs = []
    for job in self.jobs:
      if job.title not in self.applied_jobs_list(username):
        unapplied_jobs.append(job.title)
    return unapplied_jobs

  # Function to generate a list of jobs the user applied for
  def saved_jobs_list(self, username):
    applied_jobs = []
    for job_application in self.jobsSaved:
      if job_application['username'] == username:
        applied_jobs.append(job_application['job_title'])
    return applied_jobs

  # Function to print the list of jobs the user applied for
  def print_applied_jobs(self, username):
    print("Jobs you have applied for:")
    applied_jobs = self.applied_jobs_list(username)
    if applied_jobs:
      for job_title in applied_jobs:
        print("-", job_title)
    else:
      print("You haven't applied for any jobs yet.")

  # Function to print the list of jobs the user hasn't applied for
  def print_unapplied_jobs(self, username):
    print("Jobs you haven't applied for:")
    unapplied_jobs = self.unapplied_jobs_list(username)
    if unapplied_jobs:
      for job_title in unapplied_jobs:
        print("-", job_title)
    else:
      print("You have applied for all available jobs.")

  # Function to print the list of jobs the user hasn't applied for
  def print_saved_jobs(self, username):
    print("Jobs you saved:")
    saved_jobs = self.saved_jobs_list(username)
    if saved_jobs:
      for job_title in saved_jobs:
        print("-", job_title)
      response = input(
          "Do you want to unmark any saved jobs? (yes/no): ").lower()
      if response == 'yes':
        job_title_to_unmark = input(
            "Enter the title of the job you want to unmark: ")
        self.unmarkSavedJob(job_title_to_unmark)
    else:
      print("You have not saved any jobs.")

  # Function to apply for a job
  def applyForJob(self, job):
    graduation_date = input("Enter your graduation date (mm/dd/yyyy): ")
    start_date = input("Enter the date you can start working (mm/dd/yyyy): ")
    explanation = input(
        "Explain why you think you would be a good fit for this job: ")
    application_info = {
        "job_title": job.title,
        "graduation_date": graduation_date,
        "start_date": start_date,
        "explanation": explanation,
        "username": self.loggedInAcct.username
    }
    self.applications.append(application_info)
    self.saveJobApplications()
    print("Application submitted successfully!")

  #Function to save a job
  def saveAJob(self, job):
    saved_application_info = {
        "job_title": job.title,
        "username": self.loggedInAcct.username
    }
    self.jobsSaved.append(saved_application_info)
    self.saveJobsSaved()

  # Function to post about a job
  def addJobPost(self):
    if len(self.jobs) >= self.MAX_JOBS:
      print(
          "The maximum number of jobs has been reached. Please try again later."
      )
      return
    title = input("Enter the job title: ")
    description = input("Enter the job description: ")
    employer = input("Enter the employer: ")
    location = input("Enter the location: ")
    salary = input("Enter the salary: ")
    self.jobs.append(
        Job(title, description, employer, location, salary,
            self.loggedInAcct.username))
    self.saveJobPosts()
    print("Job posted successfully!")
    with open("notifications.txt", "a") as file:
      file.write(f"A new job {title} has been posted")

  #New Epic 6 Function- delete a job posting
  def deleteJobPost(self):
    title_to_delete = input("Enter the title of the job listing to delete: ")
    found = False
    for job in self.jobs:
        if job.title == title_to_delete:
            found = True
            if job.poster == self.loggedInAcct.username:
                self.jobs.remove(job)
                # Append the job title to deletion notification in the applications file
                with open('job_applications.txt', 'r+') as file:
                    lines = file.readlines()
                    file.seek(0)
                    for line in lines:
                        if title_to_delete in line.split(':'):
                            file.write(line.replace(title_to_delete, f"JOBDELETED[{title_to_delete}]"))
                        else:
                            file.write(line)
                print(f"Job listing '{title_to_delete}' deleted successfully!")
                break
    if not found:
        print(f"Job listing with title '{title_to_delete}' cannot be found.")


  # Function to display skills menu
  def skillsMenu(self):
    while True:
      print("\nWhich skill would you like to learn?")
      print("1. Digital Marketing")
      print("2. Analytical Skills")
      print("3. Technical Interview Prep")
      print("4. Leadership")
      print("5. Microsoft Excel")
      print("6. Return to the previous level")
      choice = input("\nSelect a skill to learn (1-6): ")
      if choice == '6':
        break
      elif 1 <= int(choice) <= 5:
        print("Under construction...")
      else:
        print("Invalid choice. Please enter a number between 1 and 6.")

  # Function to display Useful Links menu
  def useful_links_menu(self):
    while True:
      print("\nUseful Links:")
      print("1. General")
      print("2. Browse InCollege")
      print("3. Business Solutions")
      print("4. Directories")
      print("5. Back to Main Menu")
      choice = input("\nSelect an option (1-5): ")
      if choice == '5':
        break
      elif choice == '1':
        while True:
          print("\nGeneral:")
          print("1. Sign Up")
          print("2. Help Center")
          print("3. About")
          print("4. Press")
          print("5. Blog")
          print("6. Careers")
          print("7. Developers")
          print("8. Back to Useful Links")
          general_choice = input("\nSelect an option (1-8): ")
          if general_choice == '8':
            break
          elif general_choice == '1':
            self.run_main_menu()
          elif general_choice == '2':
            print("\nWe're here to help.")
          elif general_choice == '3':
            print(
                "\nInCollege: Welcome to InCollege, the world's largest college student network with many users in many countries and territories worldwide."
            )
          elif general_choice == '4':
            print(
                "\nInCollege Pressroom: Stay on top of the latest news, updates, and reports."
            )
          elif general_choice in ['5', '6', '7']:
            print("\nUnder construction.")
          else:
            print("\nInvalid choice. Please try again.")
      elif choice in ['2', '3', '4']:
        print("\nUnder construction.")
      else:
        print("\nInvalid choice. Please try again.")

  # Function to display InCollege Important Links menu
  def important_links_menu(self):
    while True:
      print("\nInCollege Important Links:")
      print("1. Copyright Notice")
      print("2. About")
      print("3. Accessibility")
      print("4. User Agreement")
      print("5. Privacy Policy")
      print("6. Cookie Policy")
      print("7. Copyright Policy")
      print("8. Brand Policy")
      if self.loggedInAcct:
        print("9. Languages")
        print("10. Back to Main Menu")
      else:
        print("9. Back to Main Menu")
      choice = input("\nSelect an option (1-10): ")
      if choice == '10':
        break
      elif choice == '1':
        print(
            "\nCopyright Notice: All content and materials found on the InCollege app platform, including but not limited to text, graphics, logos, images, videos, software, and any other intellectual property, are the exclusive property of InCollege or its licensors and are protected by copyright laws. Unauthorized reproduction, distribution, modification, or use of any content from the InCollege platform without the express written permission of InCollege is strictly prohibited. Users are granted a limited, non-exclusive, and non-transferable license to access and use the InCollege platform for personal and non-commercial purposes only. Any unauthorized use of the InCollege platform or its content may result in legal action. For inquiries regarding the use of InCollege's copyrighted materials or to request permission for specific uses, please contact our legal department at legalteam@incollege.com. Copyright © 2024  InCollege. All rights reserved."
        )
      elif choice == '2':
        print(
            "\nAbout: InCollege is more than an app—it's a community. Our platform is specifically tailored for college students to succeed in their academic and professional endeavors. It allows students from universities across the country to connect with each other, find resources and seek jobs. Here at InCollege, you can network with professionals, explore job postings and stay updated with academic workshops. All of this occurs in a safe and secure environment for our users. Join the millions of students who have used InCollege and paved their roads to success. Welcome to InCollege, where ambition meets opportunity!"
        )
      elif choice == '3':
        print(
            "\nAccessibility: At InCollege, inclusivity is a priority. We're committed to ensuring our platform is accessible to all users. Through features like screen reader compatibility, keyboard navigation, descriptive image text, readable color contrasts, adaptable layouts, accessible forms, and video captions, we strive to provide an inclusive experience for everyone. Your feedback is invaluable in our ongoing efforts to enhance accessibility. Please reach out to us at accessibilityteam@incollege.com with any suggestions or concerns. Together, let's build a more accessible community on InCollege"
        )
      elif choice == '4':
        print(
            "\nUser Agreement: Please read and agree to the User Agreement before using the InCollege platform."
        )
      elif choice == '5' and not self.loggedInAcct:
        print(
            "\nPrivacy Policy: InCollege respects your privacy and is committed to protecting your personal information."
        )
        break
      elif choice == '5' and self.loggedInAcct:
        print(
            "\nPrivacy Policy: InCollege respects your privacy and is committed to protecting your personal information."
        )
        if self.loggedInAcct:
          print("\nGuest Controls:")
          print("1. InCollege Email", end=" ")
          if (self.loggedInAcct.email == "email_off"):
            print("(OFF)")
          else:
            print("(ON)")

          print("2. InCollege SMS", end=" ")
          if (self.loggedInAcct.SMS == "SMS_off"):
            print("(OFF)")
          else:
            print("(ON)")
          print("3. InCollege Targeted Advertising", end=" ")
          if (self.loggedInAcct.targeted_advertising_features == "ads_off"):
            print("(OFF)")
          else:
            print("(ON)")
          print("4. Back to menu")

        guest_control = input(
            "\nSelect an option to turn off (1-3) or option 4 to go back: ")

        if guest_control == '1':
          self.loggedInAcct.email = "email_off"
          print("\nInCollege Email has been turned off.")

        elif guest_control == '2':
          self.loggedInAcct.SMS = "SMS_off"
          print("\nInCollege SMS has been turned off.")

        elif guest_control == '3':
          self.loggedInAcct.targeted_advertising_features = "ads_off"
          print("\nInCollege Targeted Advertising has been turned off.")

        elif guest_control == '4':
          continue

      elif choice == '6':
        print(
            "\nCookie Policy: At InCollege, we understand the importance of privacy and transparency when it comes to your online experience. This Cookie Policy outlines how we use cookies on our platform to enhance your browsing experience and provide personalized services. How do we use cookies? Essential Cookies: These cookies are necessary for the proper functioning of our platform. They enable core features such as user authentication and account management. Analytical Cookies: We use these cookies to gather information about how you interact with our platform. This helps us improve our services and tailor content to better meet your needs. Marketing Cookies: These cookies are used to deliver personalized advertisements based on your browsing behavior and interests. Your Cookie Choices: You have the option to accept or decline cookies when you visit our platform. However, please note that certain features may not function properly if you choose to disable cookies.Managing Cookies:You can manage cookie preferences through your browser settings. Most browsers allow you to control cookies, including blocking or deleting them altogether.By using our platform, you consent to the use of cookies in accordance with this Cookie Policy. We may update this policy from time to time, so we encourage you to review it periodically for any changes."
        )
      elif choice == '7':
        print(
            "\nCopyright Policy: InCollege respects the intellectual property rights of others and expects our users to do the same. This Copyright Policy outlines our procedures for addressing copyright infringement claims on our platform.Reporting Copyright Infringement:If you believe that your copyrighted work has been used in a way that constitutes copyright infringement on InCollege, please submit a notice of infringement to our designated Copyright Agent.In your notice, please include the following information: Identification of the copyrighted work claimed to have been infringed.Description of the infringing material and its location on our platform.Your contact information (name, address, email, phone number).A statement affirming that you have a good faith belief that the use of the material is not authorized by the copyright owner, its agent, or the law.A statement affirming that the information provided in the notice is accurate, and under penalty of perjury, that you are authorized to act on behalf of the copyright owner. Upon receiving a valid notice of infringement, we will promptly remove or disable access to the infringing material and take appropriate action in accordance with applicable laws.Counter-Notification: If you believe that the material was removed or disabled as a result of mistake or misidentification, you may submit a counter-notification to our Copyright Agent. The counter-notification must include your contact information, a description of the removed material, and a statement consenting to jurisdiction of the federal district court for the judicial district in which you are located. Please note that submitting a false claim of copyright infringement may result in legal consequences."
        )
      elif choice == '8':
        print(
            "\nBrand Policy:At InCollege, we value our brand and strive to maintain consistency and integrity in its representation across all channels. Our Brand Policy outlines the guidelines for the use of our brand assets and intellectual property.Trademark Usage: Our trademarks, logos, and brand assets are protected by law. They may only be used with our express permission and in accordance with our Brand Guidelines. Unauthorized use of our trademarks is strictly prohibited.Brand Guidelines:Our Brand Guidelines provide detailed instructions on how to use our brand assets, including logos, colors, fonts, and imagery. Adhering to these guidelines ensures that our brand is represented consistently and effectively.Co-Branding and Partnerships:Partnerships and co-branding opportunities are subject to approval by our Brand Management Team. Any use of our brand in collaboration with third parties must align with our brand values and messaging.Reporting Misuse:If you encounter unauthorized use of our brand assets or intellectual property, please report it to our Brand Protection Team. We take misuse of our brand seriously and will take appropriate action to address any violations.By using our brand assets, you agree to comply with our Brand Policy and Guidelines. Failure to adhere to these guidelines may result in legal action and termination of partnership agreements. We reserve the right to update our Brand Policy at any time to ensure consistency and protection of our brand."
        )
      elif choice == '9' and not self.loggedInAcct:
        break
      elif choice == '9' and self.loggedInAcct:
        print(
            "\nLanguages: Select your preferred language for the InCollege platform."
        )
        if (self.loggedInAcct.language == "English"):
          print("(ENGLISH)")
        else:
          print("(SPANISH)")
        language_choice = input(
            "\nSelect a language (1. English, 2. Spanish): ")
        if language_choice == '1':
          self.loggedInAcct.language = "English"
          print("\nLanguage set to English.")
        elif language_choice == '2':
          self.loggedInAcct.language = "Spanish"
          print("\nIdioma establecido en español.")
        else:
          print("\nInvalid choice. Please try again.")
      else:
        print("\nInvalid choice. Please try again.")

  # Opening Success Story to Display
  def display_welcome_message(self):
    print("\nWelcome to InCollege!")
    print("\nJane's InCollege Success Story:")
    print(
        "\nInCollege transformed my job search journey by helping me connect with professionals and discover a marketing job opportunity shared by a connection on the platform. With their support and encouragement, I not only secured the job but also found a community that empowered me to pursue my dreams with confidence. - Jane"
    )
    print("\nEmployer: Apple, Inc. Silicon Valley, California")

  # Opening Menu
  def run_main_menu(self):
    while True:
      print("\n1. Log in")
      print("2. Create an account")
      print("3. Watch Video - Why join inCollege?")
      print("4. Useful Links")
      print("5. InCollege Important Links")
      print("6. Exit")

      option = input("\nEnter your choice: ")
      if option == '6':
        self.saveAccts()
        self.saveJobPosts()
        self.saveProfiles()
        print("\nExiting InCollege. Goodbye!")
        sys.exit()
      elif option == '1':
        username = input("\nEnter your username: ")
        password = input("Enter your password: ")
        self.logIn(username, password)
        self.showOptionsMenu()
        self.saveProfiles()
      elif option == '2':
        username = input("\nEnter a username: ")
        password = input("Enter a password: ")
        first_name = input("Enter your first name: ")
        last_name = input("Enter your last name: ")
        # university = input("Enter your university: ")
        # major = input("Enter your major: ")
        self.createAcct(username, password, first_name, last_name)
      elif option == '3':
        print("\nVideo: Why join InCollege?")
        print("\n1. Play video")
        print("2. Exit")

        video_option = input("\nYour choice: ")
        if video_option == '1':
          print("\nVideo is now playing...")
        elif video_option == '2':
          print("\nExiting...")
        else:
          print("\nInvalid choice. Please try again.")
      elif option == '4':
        self.useful_links_menu()
      elif option == '5':
        self.important_links_menu()
      else:
        print("\nInvalid option. Please try again.")


if __name__ == "__main__":
  in_college_app = InCollegeAccts()
  UserAccount.set_in_college_app(in_college_app)
  in_college_app.display_welcome_message()
  in_college_app.run_main_menu()
