# from flask import Blueprint,render_template,request,redirect,url_for,session,flash
# from pymongo import MongoClient
# from .db import page2_collection,page1_collection,page3_collection

# # pdf imports
# from reportlab.lib.pagesizes import letter
# from reportlab.pdfgen import canvas
# import io
# import re
# from flask import send_file,jsonify
# import json
# from bson import ObjectId

# app_form=Blueprint('app_form',__name__)


# @app_form.route('/page1', methods=['POST', 'GET'])
# def page1():
#     # Ensure user is logged in and the application number exists in session
#     if 'application_no' not in session:
#         flash("You must be logged in to access this form.", 'danger')
#         return redirect(url_for('auth.signin'))

#     if request.method == 'POST':
#         # Extract the form data
#         application_no_input = request.form.get('applicationNo').upper().strip()  # Normalize case and strip spaces
#         session_application_no = session.get('application_no')  # Application number from the session
        
#         # Validate the application number input
#         if application_no_input != session_application_no:
#             flash("Invalid application number.", 'danger')
#             return render_template('page1.html',
#                                    application_no=session_application_no,  # Pre-fill with session-stored number
#                                    candidate_name=session.get('candidate_name', ''),
#                                    documents=session.get('documents', []),
#                                    other_documents=session.get('other_documents', ''))

#         # Get other form data
#         candidate_name = request.form.get('candidateName')
#         documents = request.form.getlist('documents')
#         other_documents = request.form.get('other_documents')

#         # Define regular expression patterns for validation
#         application_no_pattern = re.compile(r'^[A-Za-z0-9]+$')
#         candidate_name_pattern = re.compile(r'^[A-Za-z\s]+$')

#         # Validate the application number format
#         if not application_no_pattern.match(application_no_input):
#             flash("Application number should contain only letters and numbers.", 'danger')
#             return render_template('page1.html',
#                                    application_no=session_application_no,  # Pre-fill session-stored number
#                                    candidate_name=candidate_name,
#                                    documents=documents,
#                                    other_documents=other_documents)

#         # Validate the candidate's name format
#         if not candidate_name_pattern.match(candidate_name):
#             flash("Candidate's name should contain only letters.", 'danger')
#             return render_template('page1.html',
#                                    application_no=session_application_no,  # Pre-fill session-stored number
#                                    candidate_name=candidate_name,
#                                    documents=documents,
#                                    other_documents=other_documents)

#         # Check if required fields are filled
#         if not application_no_input or not candidate_name or not documents:
#             flash("Please fill out all required fields and check at least one document.", 'danger')
#             return render_template('page1.html',
#                                    application_no=session_application_no,  # Pre-fill session-stored number
#                                    candidate_name=candidate_name,
#                                    documents=documents,
#                                    other_documents=other_documents)

#         # Create a dictionary to store the extracted form data
#         form_data = {
#             "application_number": application_no_input,
#             "candidate_name": candidate_name,
#             "documents": documents,
#             "other_documents": other_documents
#         }

#         # Insert the form data into MongoDB
#         try:
#             page1_collection.insert_one(form_data)
#             # Mark the completion of this step and redirect to page2
#             # session['completed_steps'] = [1]
#             if 'progress' not in session:
#                 session['progress'] = {}
#             session['progress']['page1'] = True  # Add this to track page1 completion
#             session.modified = True  # Ensure the session is saved
#             flash('Data submitted successfully!', 'success')
#             return redirect(url_for('app_form.page2'))
#         except Exception as e:
#             flash(f"Error inserting data into MongoDB: {e}", 'danger')
#             return render_template('page1.html',
#                                    application_no=session_application_no,  # Pre-fill session-stored number
#                                    candidate_name=candidate_name,
#                                    documents=documents,
#                                    other_documents=other_documents)

#     # If it's a GET request, just render the form
#     return render_template('page1.html',
#                            application_no=session.get('application_no', ''),
#                            candidate_name=session.get('candidate_name', ''),
#                            documents=session.get('documents', []),
#                            other_documents=session.get('other_documents', ''))


# @app_form.route('/page2', methods=['POST','GET'])
# def page2():
#     if 1 not in session['completed_steps']:  
#         return redirect(url_for('app_form.page2'))
    
#     form_data = {}
    
#     if request.method=='POST':
#         # form_data = request.form.to_dict()
#         # profile_picture = request.files.get('profile_picture')

#         form_data = {
#             "application_number":session.get("application_number"),
#             "admission_type": request.form.get("admission_type"),
#             "pgcet_no": request.form.get("pgcet_no"),
#             "admission_order_no": request.form.get("admission_order_no"),
#             "rank": request.form.get("rank"),
#             "claimed_category": request.form.get("claimed_category"),
#             "allocated_category": request.form.get("allocated_category"),
#             "locality": request.form.get("admission_type"),
#             "first_name": request.form.get("first_name"),
#             "middle_name": request.form.get("middle_name"),
#             "surname": request.form.get("surname"),
#             "dob": request.form.get("dob"),
#             "gender": request.form.get("gender"),
#             "nationality": request.form.get("nationality"),
#             "religion": request.form.get("religion"),
#             "blood_group": request.form.get("blood_group"),
#             "physically_challenged": request.form.get("physically_challenged"),
#             "category": request.form.get("category"),
#             "aadhaar_no": request.form.get("aadhaar_no"),
#             "father_name": request.form.get("father_name"),
#             "mother_name": request.form.get("mother_name"),
#             "father_occupation": request.form.get("father_occupation"),
#             "mother_occupation": request.form.get("mother_occupation"),
#             "father_phone": request.form.get("father_phone"),
#             "mother_phone": request.form.get("mother_phone"),
#             "correspondence_city": request.form.get("correspondence_city"),
#             "correspondence_pincode": request.form.get("correspondence_pincode"),
#             "correspondence_state": request.form.get("correspondence_state"),
#             "correspondence_country": request.form.get("correspondence_country"),
#             "correspondence_tel": request.form.get("correspondence_tel"),
#             "correspondence_mobile": request.form.get("correspondence_mobile"),
#             "permanent_city": request.form.get("permanent_city"),
#             "permanent_pincode": request.form.get("permanent_pincode"),
#             "permanent_state": request.form.get("permanent_state"),
#             "permanent_country": request.form.get("permanent_country"),
#             "permanent_tel": request.form.get("permanent_tel"),
#             "permanent_mobile": request.form.get("permanent_mobile"),
#             "preferred_contact_time": request.form.get("preferred_contact_time"),
#             "passport": request.form.get("passport"),
#             "passport_no": request.form.get("passport_no"),
#             "passport_expiry": request.form.get("passport_expiry"),
#             "passport_issued_on": request.form.get("passport_issued_on"),
#         }

#         required_fields = [
#             "pgcet_no", "admission_order_no", "rank", 
#             "claimed_category", "allocated_category", "locality", 
#             "first_name", "surname", "dob", "gender", "nationality", 
#             "religion", "blood_group", "physically_challenged", 
#             "category", "aadhaar_no", "father_name", "mother_name", 
#             "father_occupation", "mother_occupation", "father_phone", 
#             "mother_phone", "correspondence_city", "correspondence_pincode", 
#             "correspondence_state", "correspondence_country", 
#             "correspondence_mobile", "permanent_city", "permanent_pincode", 
#             "permanent_state", "permanent_country", "permanent_mobile", 
#             "preferred_contact_time", "passport"
#         ]

#         if request.form.get("passport") == "yes":
#             required_fields += ["passport_no", "passport_expiry", "passport_issued_on"]

#         if any(form_data[field] == "" for field in required_fields):
#             flash("Please enter the details in all the required fields.", "error")
#             return render_template('page2.html', form_data=form_data)
        

#     #     return redirect(url_for('app_form.page3'))
#     # return render_template("page2.html")
#         session['completed_steps'].append(2)  # Mark section 2 as completed
#         return redirect(url_for('app_form.page3'))

#     return render_template('page2.html', form_data=form_data)


# @app_form.route('/page3',methods=['POST','GET'])
# def page3():
#     if 'signin' not in session or not session['signin']:
#         return redirect(url_for('auth.signin'))
#     if not session['progress']['page2']:
#         return redirect(url_for('app_form.page2'))
#     if request.method=='POST':
#         # save_button=request.form.get('save',None)
#         try:
#             education_data ={
#                 "10th_standard":{
#                     "course":request.form.get("course_10"),
#                     "board_university":request.form.get("board_university_10"),
#                     "college_name":request.form.get("college_name_10"),
#                     "year_from":request.form.get("year_from_10"),
#                     "year_to": request.form.get("year_to_10"),
#                     "grade": request.form.get("grade_10")
#                 },
#                 "12th_standard": {
#                     "course": request.form.get("course_12"),
#                     "board_university": request.form.get("board_university_12"),
#                     "college_name": request.form.get("college_name_12"),
#                     "year_from": request.form.get("year_from_12"),
#                     "year_to": request.form.get("year_to_12"),
#                     "grade": request.form.get("grade_12")
#                 },
#                 "graduation": {
#                     "course": request.form.get("course_ug"),
#                     "board_university": request.form.get("board_university_ug"),
#                     "college_name": request.form.get("college_name_ug"),
#                     "year_from": request.form.get("year_from_ug"),
#                     "year_to": request.form.get("year_to_ug"),
#                     "grade": request.form.get("grade_ug")
#                 },
#                 "post_graduation": {
#                     "course": request.form.get("course_pg"),
#                     "board_university": request.form.get("board_university_pg"),
#                     "college_name": request.form.get("college_name_pg"),
#                     "year_from": request.form.get("year_from_pg"),
#                     "year_to": request.form.get("year_to_pg"),
#                     "grade": request.form.get("grade_pg")
#                 },
#                 "others": {
#                     "course": request.form.get("course_ot"),
#                     "board_university": request.form.get("board_university_ot"),
#                     "college_name": request.form.get("college_name_ot"),
#                     "year_from": request.form.get("year_from_ot"),
#                     "year_to": request.form.get("year_to_ot"),
#                     "grade": request.form.get("grade_ot")
#                 }
#             }
#             work_experience_data = {
#                 'work_experience': request.form.get('work_experience'),
#                 'total_years': request.form.get('total_years'),
#                 'work_from': request.form.get('work_from'),
#                 'work_to': request.form.get('work_to'),
#                 'organization': request.form.get('organization'),
#                 'awards': request.form.get('awards'),
#                 'interests': request.form.get('interests'),
#             }

#             finance_data = {
#                 'family_income': request.form.get('family_income'),
#                 'finance_source': request.form.getlist('finance_source'),
#             }

#             entrance_test_data = {
#                 'entrance_test': request.form.getlist('entrance_test'),
#                 'other_tests_specify': request.form.get('other_tests_specify'),
#                 'test_score': request.form.get('test_score'),
#                 'registration_no': request.form.get('registration_no'),
#                 'exam_date': request.form.get('exam_date'),
#                 'no_exams': 'no_exams' in request.form,
#             }

#             # Combine all data into a single document
#             form_data = {
#                 "application_number":session.get("application_number"),
#                 'education': education_data,
#                 'work_experience': work_experience_data,
#                 'finance': finance_data,
#                 'entrance_tests': entrance_test_data,
#             }
            

#             # Insert data into MongoDB collection
#             try:
#                 page3_collection.insert_one(form_data)
#                 session['progress']['page3']=True
#                 session.modified = True
#                 return redirect(url_for('app_form.page4'))
#             except Exception as e:
#                 flash('Error While submitting the data, Please try again!',e)
#                 return redirect(url_for('app_form.page3'))
#         except Exception as e:
#             flash('Error While submitting the data, Please try again!',e)
#             return redirect(url_for('app_form.page3'))
    
#     # page2_data=session.get('page2_data',{})
#     return render_template("page3.html")

# @app_form.route('/page4',methods=['GET'])
# def page4():
#     if not session['progress']['page3']:
#         return redirect(url_for('app_form.page2'))
#     if 'signin' not in session or not session['signin']:
#         return redirect(url_for('auth.signin'))
#     return render_template("page4.html")

# # def generate_pdf(data):
# #     # Create a byte stream buffer to hold the PDF data
# #     pdf_buffer = io.BytesIO()

# #     # Create a PDF canvas
# #     pdf = canvas.Canvas(pdf_buffer, pagesize=letter)
# #     pdf.setTitle('Application Data PDF')

# #     # Add data to the PDF
# #     pdf.drawString(100, 750, 'Application Data Summary:')
    
# #     y_position = 720
# #     for collection_name, collection_data in data.items():
# #         pdf.drawString(100, y_position, f'{collection_name}: {str(collection_data)}')
# #         y_position -= 20  # Move down for the next line

# #     # Save the PDF
# #     pdf.save()

# #     # Move the buffer cursor to the beginning
# #     pdf_buffer.seek(0)

# #     return pdf_buffer

# def convert_objectid_to_str(data):
#     if isinstance(data, list):
#         return [convert_objectid_to_str(item) for item in data]
#     elif isinstance(data, dict):
#         return {key: convert_objectid_to_str(value) for key, value in data.items()}
#     elif isinstance(data, ObjectId):
#         return str(data)
#     else:
#         return data

# @app_form.route('/fetch_data',methods=['POST'])
# def fetch_data():
#     application_number=request.form.get('application_number')

#     page1_data=page1_collection.find_one({'application_number':application_number})
#     page2_data=page2_collection.find_one({'application_number':application_number})
#     page3_data=page3_collection.find_one({'application_number':application_number})

#     entireForm_data={
#         'page1_data':page1_data,
#         'page2_data':page2_data,
#         'page3_data':page3_data
#     }

#     entireForm_data = convert_objectid_to_str(entireForm_data)

#     # Create a PDF
#     pdf_buffer = io.BytesIO()
#     pdf = canvas.Canvas(pdf_buffer, pagesize=letter)
#     pdf.setTitle('Form Preview')

#     # Add content to the PDF
#     text = pdf.beginText(40, 750)  # Start position (x, y)
#     text.setFont("Helvetica", 12)

#     for page, data in entireForm_data.items():
#         text.textLine(f"{page.capitalize()}:")
#         for key, value in data.items():
#             text.textLine(f"{key}: {value}")
#         text.textLine(" ")

#     pdf.drawText(text)
#     pdf.showPage()
#     pdf.save()

#     pdf_buffer.seek(0)  # Move to the beginning of the BytesIO buffer

#     # Send the PDF to be previewed in the browser
#     return send_file(pdf_buffer, as_attachment=True, download_name='form_preview.pdf', mimetype='application/pdf')

# @app_form.route('/pdf_generator',methods=['GET'])
# def pdf_generator():
#     return render_template("pdf_generator.html")

# # @app_form.route('/download_pdf',methods=['POST'])
# # def download_pdf():
# #     data_json=request.form.get('data')
# #     if not data_json:
# #         flash("No data provided to download", 400)
# #         return '', 400

# #     try:
# #         data = json.loads(data_json)
# #     except (TypeError, json.JSONDecodeError) as e:
# #         flash(f"Invalid data format: {e}", 400)
# #         return '', 400

# #     print(data)
# #     # generate pdf
# #     pdf_buffer=generate_pdf(data)

# #     return send_file(pdf_buffer,as_attachment=True,download_name='NCET_PG_Application_form.pdf',mimetype='application/pdf')

    
# @app_form.route('/preview', methods=['POST'])
# def preview():
#     application_number = request.form.get('application_number')
#     return render_template('preview.html', application_number=application_number)


# # @app_form.route('/section1', methods=['GET', 'POST'])
# # def section1():
# #     if request.method == 'POST':
# #         # Process the form data for Section 1
# #         # ...

# #         # Update completion status
# #         session['completed_steps'] = [1]  # Mark section 1 as completed
# #         return redirect(url_for('auth.home'))

# #     return render_template('section1.html')

# # @app_form.route('/section2', methods=['GET', 'POST'])
# # def section2():
# #     # Ensure Section 1 is completed before proceeding
# #     if 1 not in session.get('completed_steps', []):
# #         return redirect(url_for('home'))

# #     if request.method == 'POST':
# #         # Process the form data for Section 2
# #         # ...

# #         # Update completion status
# #         session['completed_steps'].append(2)  # Mark section 2 as completed
# #         return redirect(url_for('auth.home'))

# #     return render_template('section2.html')



from flask import Blueprint, render_template, request, redirect, url_for, session, flash, send_file
from pymongo import MongoClient
from .db import page2_collection, page1_collection, page3_collection
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
import re
from bson import ObjectId

app_form = Blueprint('app_form', __name__)

# Utility function to convert ObjectId to string
def convert_objectid_to_str(data):
    if isinstance(data, list):
        return [convert_objectid_to_str(item) for item in data]
    elif isinstance(data, dict):
        return {key: convert_objectid_to_str(value) for key, value in data.items()}
    elif isinstance(data, ObjectId):
        return str(data)
    else:
        return data

@app_form.route('/page1', methods=['POST', 'GET'])
def page1():
    # Check if the session has 'application_no' or if it's a returning user
    # if 'application_no' not in session:
    #     flash("You must be logged in to access this form.", 'danger')
    #     return redirect(url_for('auth.signin'))

    # Initialize empty form data for GET requests
    form_data = {
        "application_number": session.get('application_no', ''),
        "candidate_name": session.get('candidate_name', ''),
        "documents": session.get('documents', []),
        "other_documents": session.get('other_documents', '')
    }

    if request.method == 'POST':
        application_no_input = request.form.get('applicationNo').upper().strip()
        # Commented out session check for demonstration
        # session_application_no = session.get('application_no')

        # Validate application number
        # if application_no_input != session_application_no:
        #     flash("Invalid application number.", 'danger')
        #     return render_template('page1.html', form_data=form_data)

        # Collect form data
        candidate_name = request.form.get('candidateName')
        documents = request.form.getlist('documents')
        other_documents = request.form.get('other_documents')

        # Update form_data for re-rendering in case of validation errors
        form_data.update({
            "application_number": application_no_input,
            "candidate_name": candidate_name,
            "documents": documents,
            "other_documents": other_documents
        })

        # Validate patterns
        application_no_pattern = re.compile(r'^[A-Za-z0-9]+$')
        candidate_name_pattern = re.compile(r'^[A-Za-z\s]+$')

        if not application_no_pattern.match(application_no_input):
            flash("Application number should contain only letters and numbers.", 'danger')
            return render_template('page1.html', form_data=form_data)

        if not candidate_name_pattern.match(candidate_name):
            flash("Candidate's name should contain only letters.", 'danger')
            return render_template('page1.html', form_data=form_data)

        if not application_no_input or not candidate_name or not documents:
            flash("Please fill out all required fields and check at least one document.", 'danger')
            return render_template('page1.html', form_data=form_data)

        # Prepare form data for storage in MongoDB
        mongo_data = {
            "application_number": application_no_input,
            "candidate_name": candidate_name,
            "documents": documents,
            "other_documents": other_documents
        }

        # Try inserting data into MongoDB
        try:
            page1_collection.insert_one(mongo_data)
            session['completed_steps'] = session.get('completed_steps', [])
            session['completed_steps'].append(1)  # Mark step 1 as completed
            session.modified = True

            # Optionally, store the form data in the session to persist across steps
            session['application_no'] = application_no_input
            session['candidate_name'] = candidate_name
            session['documents'] = documents
            session['other_documents'] = other_documents

            flash('Data submitted successfully!', 'success')
            return redirect(url_for('app_form.page2'))
        except Exception as e:
            flash(f"Error inserting data into MongoDB: {e}", 'danger')
            return render_template('page1.html', form_data=form_data)

    # Render form with session or POST data (GET request)
    return render_template('page1.html', form_data=form_data)

@app_form.route('/page2', methods=['POST', 'GET'])
def page2():
    if 'completed_steps' not in session or 1 not in session['completed_steps']:
        return redirect(url_for('app_form.page1'))

    form_data = {
        "application_number": session.get("application_no", ""),
        "admission_type": "",
        "pgcet_no": "",
        "admission_order_no": "",
        "rank": "",
        "claimed_category": "",
        "allocated_category": "",
        "locality": "",
        "first_name": "",
        "middle_name": "",
        "surname": "",
        "dob": "",
        "gender": "",
        "nationality": "",
        "religion": "",
        "blood_group": "",
        "physically_challenged": "",
        "category": "",
        "aadhaar_no": "",
        "father_name": "",
        "mother_name": "",
        "father_occupation": "",
        "mother_occupation": "",
        "father_phone": "",
        "mother_phone": "",
        "correspondence_city": "",
        "correspondence_pincode": "",
        "correspondence_state": "",
        "correspondence_country": "",
        "correspondence_tel": "",
        "correspondence_mobile": "",
        "permanent_city": "",
        "permanent_pincode": "",
        "permanent_state": "",
        "permanent_country": "",
        "permanent_tel": "",
        "permanent_mobile": "",
        "preferred_contact_time": "",
        "passport": "",
        "passport_no": "",
        "passport_expiry": "",
        "passport_issued_on": ""
    }

    if request.method == 'POST':
        # Collect form data
        form_data.update({
            "admission_type": request.form.get("admission_type"),
            "pgcet_no": request.form.get("pgcet_no"),
            "admission_order_no": request.form.get("admission_order_no"),
            "rank": request.form.get("rank"),
            "claimed_category": request.form.get("claimed_category"),
            "allocated_category": request.form.get("allocated_category"),
            "locality": request.form.get("locality"),
            "first_name": request.form.get("first_name"),
            "middle_name": request.form.get("middle_name"),
            "surname": request.form.get("surname"),
            "dob": request.form.get("dob"),
            "gender": request.form.get("gender"),
            "nationality": request.form.get("nationality"),
            "religion": request.form.get("religion"),
            "blood_group": request.form.get("blood_group"),
            "physically_challenged": request.form.get("physically_challenged"),
            "category": request.form.get("category"),
            "aadhaar_no": request.form.get("aadhaar_no"),
            "father_name": request.form.get("father_name"),
            "mother_name": request.form.get("mother_name"),
            "father_occupation": request.form.get("father_occupation"),
            "mother_occupation": request.form.get("mother_occupation"),
            "father_phone": request.form.get("father_phone"),
            "mother_phone": request.form.get("mother_phone"),
            "correspondence_city": request.form.get("correspondence_city"),
            "correspondence_pincode": request.form.get("correspondence_pincode"),
            "correspondence_state": request.form.get("correspondence_state"),
            "correspondence_country": request.form.get("correspondence_country"),
            "correspondence_tel": request.form.get("correspondence_tel"),
            "correspondence_mobile": request.form.get("correspondence_mobile"),
            "permanent_city": request.form.get("permanent_city"),
            "permanent_pincode": request.form.get("permanent_pincode"),
            "permanent_state": request.form.get("permanent_state"),
            "permanent_country": request.form.get("permanent_country"),
            "permanent_tel": request.form.get("permanent_tel"),
            "permanent_mobile": request.form.get("permanent_mobile"),
            "preferred_contact_time": request.form.get("preferred_contact_time"),
            "passport": request.form.get("passport"),
            "passport_no": request.form.get("passport_no"),
            "passport_expiry": request.form.get("passport_expiry"),
            "passport_issued_on": request.form.get("passport_issued_on"),
        })

        # Debugging: Print form data
        print("Form Data Received:", form_data)

        required_fields = [
            "pgcet_no", "admission_order_no", "rank", 
            "claimed_category", "allocated_category", "locality", 
            "first_name", "surname", "dob", "gender", "nationality", 
            "religion", "blood_group", "physically_challenged", 
            "category", "aadhaar_no", "father_name", "mother_name", 
            "father_occupation", "mother_occupation", "father_phone", 
            "mother_phone", "correspondence_city", "correspondence_pincode", 
            "correspondence_state", "correspondence_country", 
            "correspondence_mobile", "permanent_city", "permanent_pincode", 
            "permanent_state", "permanent_country", "permanent_mobile", 
            "preferred_contact_time", "passport"
        ]

        if form_data.get("passport") == "yes":
            required_fields += ["passport_no", "passport_expiry", "passport_issued_on"]

        # Check for missing required fields
        if any(not form_data.get(field) for field in required_fields):
            flash("Please enter the details in all the required fields.", "error")
            return render_template('page2.html', form_data=form_data)

        # Save the form data into MongoDB
        try:
            page2_collection.insert_one(form_data)
            session['completed_steps'].append(2)  # Mark section 2 as completed
            session.modified = True

            flash("Data submitted successfully!", "success")
            return redirect(url_for('app_form.page3'))
        except Exception as e:
            flash(f"Error inserting data into MongoDB: {e}", "danger")
            return render_template('page2.html', form_data=form_data)

    # Render page2 form
    return render_template('page2.html', form_data=form_data)

@app_form.route('/page3', methods=['POST', 'GET'])
def page3():
    if 'signin' not in session or not session.get('signin'):
        return redirect(url_for('auth.signin'))
    if not session.get('completed_steps') or 2 not in session['completed_steps']:
        return redirect(url_for('app_form.page2'))

    form_data = {}

    if request.method == 'POST':
        # Collect data for page 3
        form_data = {
            "application_number": session.get("application_no"),
            "additional_info": request.form.get("additional_info")  # Add fields for page3
            # Add more fields as per your requirements
        }

        # Save the form data into MongoDB
        try:
            page3_collection.insert_one(form_data)
            session['completed_steps'].append(3)  # Mark section 3 as completed
            session.modified = True

            flash("Data submitted successfully!", "success")
            # Redirect to next step or final page
            return redirect(url_for('app_form.final_page'))
        except Exception as e:
            flash(f"Error inserting data into MongoDB: {e}", "danger")
            return render_template('page3.html', form_data=form_data)

    # Render page3 form
    return render_template('page3.html', form_data=form_data)

@app_form.route('/page4', methods=['GET'])
def page4():
    # Ensure step 3 is completed
    if not session.get('completed_steps') or 3 not in session['completed_steps']:
        return redirect(url_for('app_form.page3'))
    
    return render_template("page4.html")

@app_form.route('/fetch_data', methods=['POST'])
def fetch_data():
    application_number = request.form.get('application_number')

    # Fetch data from MongoDB
    page1_data = page1_collection.find_one({'application_number': application_number})
    page2_data = page2_collection.find_one({'application_number': application_number})
    page3_data = page3_collection.find_one({'application_number': application_number})

    # Convert ObjectId to string
    page1_data = convert_objectid_to_str(page1_data)
    page2_data = convert_objectid_to_str(page2_data)
    page3_data = convert_objectid_to_str(page3_data)

    if page1_data and page2_data and page3_data:
        return {
            'page1_data': page1_data,
            'page2_data': page2_data,
            'page3_data': page3_data
        }
    return {'error': 'No data found.'}