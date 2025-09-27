### Abstractclass 
import json
import os
import abc
class Employee(abc.ABC):
    def __init__(self, employee_id:str, name: str ,department:str):
        self._employee_id = employee_id
        self._name = name
        self._department = department
    @property
    def employee_id(self):
        return self._employee_id
    @property
    def name(self):
        return self._name
    @property
    def department(self):
        return self._department
    @department.setter 
    def department(self,department:str):
        self._department = department
        
    @abc.abstractmethod
    def calculate_salary(self)-> float:
        pass
    def display_details(self) -> str:
        return f"ID:{self._employee_id},Name: {self._name},Dept: {self._department}"
    def to_dict(self) -> dict:
        return { 
            'employee_id' : self._employee_id,
            'name' : self._name,
            'department' : self._department
        }
#full time employee class
class FulltimeEmployee(Employee):

    def __init__(self,employee_id:str, name:str, department:str, monthly_salary:float):
        super().__init__(employee_id, name, department)
        self._monthly_salary=0.0 
        self.monthly_salary= monthly_salary

    @property
    def monthly_salary(self)-> float:
        return self._monthly_salary

    @monthly_salary.setter 
    def monthly_salary(self,value:float):
        
        if value<0:
            raise ValueError("Monthly salary can not be negative")
        self._monthly_salary= value

    def calculate_salary(self)->float:
        return self._monthly_salary

    def display_details(self)->str:
        detail1= super().display_details()
        return f"{detail1}, Salary:{self.monthly_salary}"

    def to_dict(self)->dict:
        data = super().to_dict()
        data['monthly_salary']=self.monthly_salary
        data['employee_type'] = "Full Time"
        return data


class ParttimeEmployee(Employee):

     def __init__(self,employee_id:str, name:str, department:str, hourly_rate:float, hours_worked_per_month:float):
        super().__init__(employee_id, name, department)
        self._hourly_rate= 0.0
        self._hours_worked_per_month=0.0
        self.hourly_rate= hourly_rate
        self.hours_worked_per_month= hours_worked_per_month

     @property
     def hourly_rate(self)->float:
         return self._hourly_rate

     @hourly_rate.setter
     def hourly_rate(self,value:float):
      
        if value<0:
            raise ValueError("Hourly rate can't be negative")
        self._hourly_rate= value

     @property
     def hours_worked_per_month(self)->float:
         return self._hours_worked_per_month

     @hours_worked_per_month.setter
     def hours_worked_per_month(self,value:float):
         if value<0:
             raise ValueError("Hours worked can't be negative")
         self._hours_worked_per_month= value

     def calculate_salary(self)->float:
         return self.hourly_rate* self.hours_worked_per_month

     def display_details(self)->str:
         detail2= super().display_details()
         return f"{detail2}, Hourly Rate:{self.hourly_rate}, Hours Worked: {self.hours_worked_per_month},Salary:{self.calculate_salary()}"

     def to_dict(self)->dict:
         data= super().to_dict()
         data['hourly_rate']= self.hourly_rate
         data["hours_worked_per_month"]= self.hours_worked_per_month
         data["salary"]= self.calculate_salary()
         data['employee_type'] = "Part Time"
         return data

class Manager(FulltimeEmployee):
     def __init__(self,employee_id:str, name:str, department:str, monthly_salary:float, bonus:float):
         super().__init__(employee_id, name, department, monthly_salary)
         self._bonus= 0.0
         self.bonus= bonus

     @property
     def bonus(self)->float:
         return self._bonus

     @bonus.setter
     def bonus(self,value:float):
         if value<0:
             raise ValueError("bonus worked can't be negative")
         self._bonus= value

     def calculate_salary(self)->float:
         return super().calculate_salary() + self.bonus

     def display_details(self)->str:
         detail3= super().display_details().split(',Salary:')[0]
         return f"{detail3}, Bonus:{self.bonus}, Total Salary:{self.calculate_salary()}"

     def to_dict(self)->dict:
         data= super().to_dict()
         data["bonus"]= self.bonus
         data["salary"]= self.calculate_salary()
         data['employee_type']= "Manager"
         return data
        
class Company:
     def __init__(self, data_file:str='employees.json'):
         self._employees={}
         self.data_file= data_file
         self._load_data()
     def _load_data(self)->None:
         if os.path.exists(self.data_file):
             try:
                 with open(self.data_file, 'r') as f:
                     raw_data= json.load(f)

                     for emp_id, emp_data in raw_data.items():
                         employee_type= emp_data.get('employee_type')
                         department= emp_data.get('department','Unknown')
                         if employee_type == 'Full Time':
                             self._employees[emp_id]= FulltimeEmployee(
                                 employee_id= emp_data['employee_id'],
                                 name=emp_data['name'],
                                 department=emp_data['department'],
                                 monthly_salary=emp_data['monthly_salary'])
                         elif employee_type == 'Part Time':
                             self._employees[emp_id]= ParttimeEmployee(
                                 employee_id= emp_data['employee_id'],
                                 name=emp_data['name'],
                                 department=emp_data['department'],
                                 hourly_rate=emp_data['hourly_rate'],
                                 hours_worked_per_month=emp_data["hours_worked_per_month"])
                         elif employee_type == 'Manager':
                             self._employees[emp_id]=Manager(
                                 employee_id= emp_data['employee_id'],
                                 name=emp_data['name'],
                                 department=emp_data['department'],
                                 monthly_salary=emp_data['monthly_salary'],
                                 bonus=emp_data['bonus']
                                 )
                         else:
                             print(f"Warning: Unknown employee type'{employee_type}' for ID'{emp_id}'.Skipping")
                        
             except json.JSONDecodeError:
                 print(f"Error: Data file {self.data_file} contains invalid JSON. Starting with empty employee data.")
             except FileNotFoundError:
                 print(f"Info: Data file '{self.data_file}' not found. Starting with empty employee data")
             except KeyError as e:
                 print(f"Error loading employee data: Missing key {e} for employee ID {emp_id}. Skipping.")
         else:
             print(f"Info: Data file '{self.data_file}' not found. Starting with empty employee data.")

     def _save_data(self)->None:
         serializable_data={}
         for emp_id, employee_obj in self._employees.items():
             serializable_data[emp_id]= employee_obj.to_dict()
         try:
             with open(self.data_file,'w') as f:
                 json.dump(serializable_data, f, indent=4)
             print(f"Data successfully saved to {self.data_file}")
         except Exception as e:
             print(f"Error saving data to {self.data_file}:{e}")

     def add_employee(self, employee)->bool:
         if employee.employee_id in self._employees:
             
             print(f" Employee with ID{employee.employee_id} already exists")
             return False
         else:
             self._employees[employee.employee_id]= employee
             self._save_data()
             print(f" Employee {employee.name} (ID:{employee.employee_id} added successfully")
             return True

     def remove_employee(self, employee_id:str)->bool:
         if employee_id in self._employees:
             employee_name= self._employees[employee_id].name
             del self._employees[employee_id]
             self._save_data()
             print(f" Employee {employee_name} (ID:{employee_id}) removed successfully")
             return True
         else:
             print(f" Employee with ID{employee_id} not found")
             return False
             
     def find_employee(self, employee_id:str)->Employee|None:
         employee= self._employees.get(employee_id)
         if employee:
             print(f" Employee {employee.name} (ID:{employee.employee_id}) found")
             
         else:
             print(f"Employee with ID{employee_id} not found")
         return employee
         
     def calculate_total_payroll(self)->float:
         total_payroll=0.0
         for employee in self._employees.values():
             total_payroll+=employee.calculate_salary()
         return total_payroll

     def display_all_employees(self)->None:
         print("\n----Current Employees----")
         for employee in self._employees.values():
             print(employee.display_details())
         print("---------------------")

     def generate_payroll_report(self)->None:
         print("\n---payroll report----")
         if not self._employees:
             print("no employees to generate a payroll report for")
             return
         print(f"{'ID':} {'Name':} {'Type':} {'Salary':}")
         total_payroll = 0.0
         for employee in self._employees.values():
             salary= employee.calculate_salary()
             total_payroll+=salary
             employee_type= employee.to_dict().get('employee_type')
             print(f"{employee.employee_id:}{employee.name:}{employee_type:}{salary:}")
         print(f"{'Total Payroll:'} {total_payroll:}")
         print("-------------------")
        
def main():
    company = Company()
    while True:
        print("1. Add Employee")
        print("2. View All Employee")
        print("3. Calculate Total Payroll")
        print("4. Search Employee")
        print("5. Remove Employee") 
        print("6. payroll report")
        print("7. exit")

        choice = input("Enter you choice:")
        
        if choice == '1':
            emp_type = input("Enter employee type:")
            emp_id = input("Enter employee ID:")
            name  = input("Enter employee name:")
            department= input("Enter Department:")
            employe= None
            try:
                if emp_type == 'Full Time':
                    salary = float(input("Enter Monthly salary:"))
                    employee = FulltimeEmployee(emp_id,name,department,salary)
                elif emp_type == 'Part Time':
                    hourly_rate = float(input("Enter Hourly Rate: "))
                    hours_worked = float(input("Enter Hours Worked: "))
                    employee = ParttimeEmployee(emp_id, name, department, hourly_rate, hours_worked)
                elif emp_type == 'Manager':
                    monthly_salary = float(input("Enter Monthly Salary: "))
                    bonus = float(input("Enter Bonus: "))
                    employee = Manager(emp_id, name,department, monthly_salary, bonus)
                else:
                    print("Invalid employee type.")
                    continue
                if employee:
                    company.add_employee(employee)
                    print("Employee added successfully.")
            except ValueError as e:
                print(f"Error:{e}. Please enter valid numeric values.")

        elif choice == '2':
            company.display_all_employees()

        elif choice == '3':
            total_payroll = company.calculate_total_payroll()
            print(f"Total Payroll: {total_payroll}")

        elif choice == '4':
            search_choice = input("Search by (id/name): ")
            if search_choice == 'id':
                emp_id = input("Enter Employee ID: ")
                company.find_employee(emp_id)

            elif search_choice=='name' :
                emp_name= input("Enter Employee Name:")
                company.find_employee(emp_name)
            
            else:
                print("Invalid search choice.")

        elif choice == '5':
            emp_id = input("Enter Employee ID to remove: ")
            company.remove_employee(emp_id)
            print("Employee removed successfully.")

        elif choice=='6':
            company.generate_payroll_report()

        elif choice == '7':
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main()        
        
        
            
        
        
    
        
        
        
    
    
    
        
