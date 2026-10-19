from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestMusicSchoolCourse(TransactionCase):

    # Se ejecuta UNA vez antes de todos los tests: datos comunes.
    # Cada test se ejecuta dentro de una transacción que al final se deshace,
    # así que nada de esto se queda guardado en la base de datos.
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.teacher = cls.env['music.school.teacher'].create({
            'name': 'Test Teacher',
            'level': 'beginner',
        })
        cls.course = cls.env['music.school.course'].create({
            'name': 'Test Guitar Course',
            'teacher_id': cls.teacher.id,
            'capacity': 2,
            'state': 'progress',
        })
        # Con la delegación, al crear el alumno se crea solo su contacto
        cls.students = cls.env['music.school.student'].create([
            {'name': 'Test Student 1'},
            {'name': 'Test Student 2'},
            {'name': 'Test Student 3'},
        ])

    def test_assign_students(self):
        """Asigna alumnos sin pasar de la capacidad y sin duplicarlos."""
        self.course.assign_students()
        self.assertEqual(len(self.course.student_ids), 2,
                         "Debe asignar tantos alumnos como la capacidad del curso")

        # Pulsar otra vez no debe duplicar alumnos (Command.link)
        self.course.assign_students()
        self.assertEqual(len(self.course.student_ids), 2)

    def test_action_finish(self):
        """Finaliza el curso y sus lecciones, salvo las canceladas."""
        Lesson = self.env['music.school.lesson']
        lesson_scheduled = Lesson.create({'course_id': self.course.id})
        lesson_cancelled = Lesson.create({'course_id': self.course.id, 'state': 'cancelled'})

        self.course.action_finish()

        self.assertEqual(self.course.state, 'finished')
        self.assertEqual(lesson_scheduled.state, 'done')
        self.assertEqual(lesson_cancelled.state, 'cancelled',
                         "Una lección cancelada no debe pasar a realizada")

    def test_create_lesson(self):
        """Crea una lección del curso con el profesor del curso."""
        Lesson = self.env['music.school.lesson']
        domain = [('course_id', '=', self.course.id)]
        lessons_before = Lesson.search_count(domain)

        self.course.create_lesson()

        self.assertEqual(Lesson.search_count(domain), lessons_before + 1)
        lesson = Lesson.search(domain, order='id desc', limit=1)
        self.assertEqual(lesson.teacher_id, self.teacher)
        self.assertEqual(lesson.state, 'scheduled')
