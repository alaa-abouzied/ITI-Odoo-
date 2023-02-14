from odoo import fields,models,api
from odoo.exceptions import UserError




class ItiStudent(models.Model):
    _name = "iti.student"
    
    name = fields.Char(required=True)
    email = fields.Char()
    birth_date = fields.Date()
    salary = fields.Float()
    tax = fields.Float(compute=("calc_salary"),store=True)
    net_salary = fields.Float(compute=("calc_salary"),store=True)
    address = fields.Text()
    gender = fields.Selection([('m',"Male"),('f',"Female")])
    accepted = fields.Boolean()
    level = fields.Integer()
    image = fields.Binary()
    cv = fields.Html()
    login_time = fields.Datetime()
    track_id = fields.Many2one("iti.track")
    track_capacity = fields.Integer(related='track_id.capacity')
    skills_ids = fields.Many2many("iti.skill")
    grade_ids = fields.One2many("student.grade.line","student_id")
    state = fields.Selection([
        ('applied','Applied'),
        ('first','First Interview'),
        ('second','Second Interview'),
        ('passed','Passed'),
        ('rejected','Rejected')
        ],default='applied')
    
    @api.depends("salary") #m3naha l function dy hy7slha update lma l salary yt8ir
    def calc_salary(self):
        for student in self:
            student.tax = student.salary * 0.20
            student.net_salary = student.salary - student.tax
    
    @api.model
    def create(self, vals): #vals l data bta3t l form byb3tha automatic 3la shakl dictionary
        # new_student=super().create(vals)
        # name_split = new_student.name.split()
        name_split = vals['name'].split() #== new_student=super().create(vals) and name_split = new_student.name.split()
        vals['email'] = f"{name_split[0][0]}{name_split[1]}@gmail.com"
        search_students = self.search([('email','=',vals['email'])],limit=1)
        # self.env['iti.track'].search() --->dy bst5dmha 3shan adwar f model tany 8ir elly ana wa2fa fyh y3ny hena 2oltlo ana wa2fa f table l student bs ro7 dwar f table(model) iti.track
        track = self.env['iti.track'].browse(vals['track_id'])
        if track.is_open is False:
            raise UserError("This track is closed")      
        # if search_students:
        #     raise UserError("This E-mail is aleady exist.")
        # return new_student
        return super().create(vals)
    
   
    def write(self, vals):
        if "name" in vals:
            name_split = vals['name'].split() #== new_student=super().create(vals) and name_split = new_student.name.split()
            vals['email'] = f"{name_split[0][0]}{name_split[1]}@gmail.com"
        super().write(vals)
        
        
    def unlink(self):
        for student in self:
            if student.state in ['passed', 'rejected']:
                raise UserError("u can't delete passed or rejected students")
        super().unlink()
    
    _sql_constraints = [
        ("UniqueName","UNIQUE(name)","This name is Exist")
    ]   
    
    @api.constrains("track_id")
    def check_capacity(self):
        track_count = len(self.track_id.student_ids)
        track_capacity = self.track_id.capacity
        if track_count > track_capacity:
            raise UserError("Track is FULL")          

    @api.constrains("salary")
    def check_salary(self):
        if self.salary > 10000:
            raise UserError("salary can't be greater than 10000")
    
    def change_state(self):
        if self.state == 'applied':
            self.state = 'first'    
        elif self.state == 'first':
            self.state = 'second'
        elif self.state in ['passed','rejected']:
            self.state = 'applied'  
            
    def set_passed(self):
        self.state = 'passed'    
    
    def set_rejected(self):
        self.state = 'rejected'
            
                  
    @api.onchange("gender")
    def _on_change_gender(self):
        domain = {'track_id':[]}
        if not self.gender:
            self.gender = "f"
            return {}
        if self.gender == 'm':
            domain = {'track_id':[('is_open','=',True)]}
            self.salary = 700000
        else:
            self.salary = 900000
        return {
            'warning':{
                'title':'Hello',
                'message':'U have changed the gender'
            },
            'domain':domain
        }
         
    
class ItiCourse(models.Model):
    _name = 'iti.course'
    
    name = fields.Char()
    
class StudentCourseGrades(models.Model):
    _name = 'student.grade.line'
    
    student_id = fields.Many2one("iti.student")
    course_id = fields.Many2one("iti.course")
    grade = fields.Selection([("g","good"),("v","very good")])    