# commutr

**safe, organized carpooling for parents who value community.**

![commutr Dashboard](assets/logo/better_pool_logo.png)

---

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34C26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)

---

## What and why?

School drop-offs are chaos. Parents scramble daily to arrange rides, text multiple people, and hope someone shows up. Kids are left waiting. Schedules conflict. Safety is a question mark.

What if there was a single, organized place where parents could create carpools, find nearby groups heading to the same school, and manage everything in one app? No more fragmented texts. No more guessing who's picking up who. Just reliable, verified carpooling.

**commutr** brings structure to the carpool. It's a platform where parents can create groups, invite others nearby, and coordinate school transportation with confidence — knowing exactly who's in the car and when to expect pickup.

---

## Features

- **Parent Authentication & Profiles:** Secure signup with verification. Parents create profiles with phone, address, neighborhood, and verified status.
- **School Management:** Browse and filter by school. Carpools are organized by destination, making it easy to find groups heading where you need.
- **Carpool Groups:** Create groups as a driver or join as a passenger. Each group has a driver, capacity limit, and scheduled pickup/dropoff times.
- **Smart Search:** Find carpools by neighborhood and school. Intelligent filtering shows available groups near you.
- **Child Enrollment:** Link children to their schools and programs. The system tracks which kids belong to which carpools.
- **Capacity Management:** Groups have max capacity limits, preventing overcrowding and ensuring safe rides.
- **Organized Dashboard:** View all active carpools, passenger lists, and schedules in one place.

---

## How it works

**commutr** operates as a straightforward, user-centric platform built around three core entities: Parents, Schools, and Carpool Groups.

1. **Parent Registration (`/signup`):** Parents create an account with their personal and address information. This data forms the foundation for matching and search.
2. **Child Setup:** Parents add their children, assigning them to schools and programs. This links families to specific school routes.
3. **School & Carpool Discovery:** Parents browse the list of available schools and search for existing carpool groups by neighborhood and school name.
4. **Create or Join Groups:** As a driver, a parent can create a new carpool group with pickup/dropoff times and passenger capacity. As a passenger, they can join existing groups heading their direction.
5. **Dashboard & Management:** The dashboard displays all joined and driving groups, making it simple to see schedules and passenger lists at a glance.

### Flow Diagram

```
Parent Signs Up
     │
     ▼
Add Children to Schools
     │
     ▼
Browse Schools & Search Carpools
     │
     ├──► Create New Carpool Group (as Driver)
     │
     └──► Join Existing Carpool Group (as Passenger)
     │
     ▼
Dashboard – View & Manage Groups
```

---

## Tech stack

**commutr** is built on Django, a robust Python web framework designed for rapid development and maintainability.

| Layer                | Technology | Purpose                                                |
| :------------------- | :--------- | :----------------------------------------------------- |
| **Backend**          | Django     | Web framework for API, views, and business logic       |
| **Database**         | SQLite     | Lightweight database for development and deployment    |
| **Frontend**         | HTML/CSS   | Responsive templates for browser-based user interface  |
| **Authentication**   | Django Auth | Built-in user management with login and signup        |
| **ORM**              | Django ORM | Object-relational mapping for database queries         |
| **Language**         | Python 3   | Core programming language                             |

---

## Running locally

### Prerequisites

- **Python 3.8+**
- **pip** or **uv** package manager
- **Git** (optional, for cloning)

### Setup

1. **Clone or Extract the Project:**

   ```bash
   git clone https://github.com/your-username/commutr.git
   cd commutr
   ```

2. **Create a Virtual Environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

   Or using **uv** (faster):

   ```bash
   uv pip install -r requirements.txt
   ```

4. **Apply Database Migrations:**

   ```bash
   python manage.py migrate
   ```

5. **Load Sample Data (Optional):**

   ```bash
   python manage.py seed_data
   ```

6. **Create a Superuser (Optional):**

   ```bash
   python manage.py createsuperuser
   ```

7. **Run the Development Server:**

   ```bash
   python manage.py runserver
   ```

   The app will be available at `http://localhost:8000`

---

## Data Model

**commutr** uses a relational data model centered on parents, schools, and carpool groups:

```
School
├── id, name, address, city, region_code

ParentProfile
├── user (OneToOne → User)
├── phone_number, home_address, city, neighborhood
├── is_verified

Child
├── parent (ForeignKey → ParentProfile)
├── first_name, age
├── school (ForeignKey → School)
├── program_enrolled

CarpoolGroup
├── name, school (ForeignKey → School)
├── driver (ForeignKey → ParentProfile)
├── passengers (ManyToMany → ParentProfile)
├── max_capacity, pickup_time, dropoff_time
├── created_at
```

Each **CarpoolGroup** connects a driver to multiple passengers, all heading to the same school at coordinated times.

---

## Project Structure

```
commutr/
├── carpool/                          # Main Django app
│   ├── models.py                     # Data models
│   ├── views.py                      # View logic
│   ├── urls.py                       # URL routing
│   ├── admin.py                      # Admin interface
│   ├── templates/carpool/            # HTML templates
│   │   ├── index.html
│   │   ├── dashboard.html
│   │   ├── group.html
│   │   ├── results.html
│   │   ├── signup.html
│   │   └── login.html
│   ├── static/carpool/               # CSS and assets
│   │   └── styles.css
│   └── management/commands/
│       └── seed_data.py              # Data seeding command
├── core/                             # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py                         # Django CLI
├── db.sqlite3                        # SQLite database
└── README.md
```

---

## Notes

- **Verification:** The `is_verified` field on `ParentProfile` can be used to implement background checks or email verification in the future.
- **Seed Data:** Run `python manage.py seed_data` to populate the database with sample schools, parents, children, and carpool groups for testing.
- **Admin Panel:** Access the Django admin at `/admin` (after creating a superuser) to manage all data directly.
- **Scalability:** SQLite works great for development and small deployments. For production, migrate to PostgreSQL or MySQL.

---

## What's next

The platform is fully functional and ready to use, but there's plenty of room to grow:

- [ ] **Parent Verification:** Implement background checks and email/phone verification
- [ ] **Ratings & Reviews:** Parents rate drivers and experience after each carpool
- [ ] **Real-time Availability:** Show live pickup locations using GPS integration
- [ ] **Notifications:** SMS/email alerts for schedule changes and pickup times
- [ ] **Payment Integration:** Built-in payment for gas sharing or child care costs
- [ ] **Mobile App:** React Native or Flutter app for on-the-go access
- [ ] **Multi-language Support:** Localization for diverse neighborhoods
- [ ] **Incident Reporting:** Safe way to report issues or concerns
- [ ] **Group Chat:** In-app messaging for driver-passenger communication
- [ ] **Analytics Dashboard:** Parents see trends, savings, and environmental impact

---

<div align="center">

_because raising kids takes a village._ 🏘️

_commutr brings that village to your phone._

</div>
