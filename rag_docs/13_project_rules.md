# ProjectPartner — Core Platform Rules

These are the fundamental rules that define how ProjectPartner works.  
The assistant must strictly follow these rules whenever answering.

---

## 1. Project Deletion
- **Projects cannot be deleted under any circumstances.**
- Once created, a project remains permanently visible on the platform.
- Authors can update project details, but deletion is not allowed.

---

## 2. Closing a Project
- Only the **project author** can close their project.
- Closing a project means:
  - The project remains visible on the platform.
  - **No new join requests** can be sent.
- Closed projects can still be viewed by everyone.

---

## 3. Join Requests
- Logged-in users can send join requests to open projects.
- Guests cannot send join requests.
- **Project authors** have the ability to:
  - Accept join requests  
  - Decline join requests  

---

## 4. Project Creation
- Only **logged-in users** can create and post new projects.
- Guests cannot create or manage projects.
- Required fields for creating a project:
  - Project Title
  - Project Description
  - Required Skills
  - Tech Stack
  - Optional: Project Image

---

## 5. Guest Limitations
Guests CANNOT:
- Post projects  
- Send join requests  
- Send messages  
- Access features requiring authentication  

Guests CAN:
- Browse projects
- View project details

---

## 6. Messaging Rules
- Only logged-in users can send messages.
- Users can only message authors or teammates of the projects they join.

---

## 7. Profile Editing Rules
- Users can edit most profile details anytime.
- **Email cannot be changed** after account creation.

---

## 8. Visibility Rules
- All projects (open or closed) stay visible to all users.
- Users can view:
  - Project Title  
  - Project Description  
  - Required Skills  
  - Tech Stack  
  - Author info (limited)  
  - Project status (open/closed)

---

## 9. Author Permissions
A project author can:
- Edit their project details
- Accept or decline join requests
- Close their project
- Message teammates

A project author CANNOT:
- Delete their project
- Remove project visibility from platform

---

## 10. Platform Behaviors (Always True)
- A closed project does **not** accept join requests.
- A deleted project does **not exist** because deletion is not supported.
- Profile edits update instantly across the platform.

---

## 11. Safety Rules for the Chatbot
The assistant must:
- **Never invent new features**
- **Never assume UI steps not defined in documentation**
- **Never mention “documentation says…” or “not listed in docs”**
- **Stick strictly to these rules and RAG context**

