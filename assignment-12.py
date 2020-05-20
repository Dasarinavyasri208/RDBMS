class DoesNotExist(Exception):
	pass
class Student:
	def __init__(self, name, age, score):
		self.name = name
		self.student_id = None
		self.age = age
		self.score = score
		
	@staticmethod
	def get(student_id=0,name="",score=-1,age=0):
		if student_id != 0:
			record = read_data(f"select * from Student where student_id={student_id}")
		elif name != "":
			record = read_data(f"select * from Student where name={name}")
		elif score != -1:
			record = read_data(f"select * from Student where score={score}")
		elif age != 0:
			record = read_data(f"select * from Student where age={age}")
		
		if len(record)==0:
			raise Exception('DoesNotExist')
		elif len(record)>1:
			raise Exception('MultipleObjectsReturned')
		else:
			output = Student(record[0][1],record[0][2],record[0][3])
			output.student_id = record[0][0]
			return output
		
	def save(self):
		write_data(f"insert into Student (name,age,score) values (\'{self.name}\',{self.age},{self.score})")        
		
	def delete(self):
		pass

	def filter(self):
		pass

def write_data(sql_query):
	import sqlite3
	connection = sqlite3.connect("students.sqlite3")
	crsr = connection.cursor() 
	crsr.execute("PRAGMA foreign_keys=on;") 
	crsr.execute(sql_query) 
	connection.commit() 
	connection.close()

def read_data(sql_query):
	import sqlite3
	connection = sqlite3.connect("students.sqlite3")
	crsr = connection.cursor()
	crsr.execute(sql_query) 
	ans= crsr.fetchall()  
	connection.close() 
	return ans


#student_obj = Student(name="mahi",age=22,score=98)
#student_obj.save()
'''s=Student.get(student_id=11)
print(s.name)
print(s.student_id)
print(read_data("SELECT * FROM student"))'''   
