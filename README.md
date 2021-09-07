# Meeter

#### Video Demo: <url>

#### Description:

##### About

Meeter is a flask based web application that can help you manage meeting invites for school.

##### Working

Meeter uses regex to split, identify and categorise meeting invites from input text.

To use, follow these steps:

1. Login/Register into Meeter.
2. Tap on “Add My Meetings” card.
3. Select all your meeting links, messages etc. *all at once*, and paste them into “Paste Meeting Invites Here” box.
4. Let the dropdown remain at Tomorrow if you’re adding invites a day before, or set it to Today if links are to be used today.
5. Voila! All your meetings with appropriate time, date and links will be displayed!

The cards are themed - green for Google Meet links, and blue for Zoom links. The cards will also display GMeet Code for Google Meet, and Meeting ID + Passcode for Zoom.

##### Additional Features

###### Edit

After you have added your Meetings, you can tap on edit to access the edit page. Here you can edit the meeting data like time, subject, teacher name etc. in case they couldn’t be identified.

You can also delete messages from herein.

###### **Suggestions**

Meeter intelligently remembers your meetings from last week. Thus, if you log in after a week, instead of being greeted by a blank pages, you’ll see all the cards you saw last week on the same way.

Weekly suggestions were implemented keeping in mind the time tables of school - they largely remain fixed throughout the week.

The “Add My Meetings” feature is still available, so in case of a change in schedule/different links etc. new meetings can be added.

Freshly added meetings are always preferred over Suggestions, so when new meetings are added, Suggestions are hidden.