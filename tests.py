import pytest
from model import Question


def test_create_question():
    question = Question(title='q1')
    assert question.id is not None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct

# 1
def test_remove_choice_using_id():
    question = Question(title='q2')
    choice1 = question.add_choice('a')
    choice2 = question.add_choice('b')
    choice3 = question.add_choice('c')

    question.remove_choice_by_id(choice2.id)

    assert [choice.id for choice in question.choices] == [choice1.id, choice3.id]

# 2
def test_remove_all_choices():
    question = Question(title='q2')
    question.add_choice('a')
    question.add_choice('b')
    question.add_choice('c')

    question.remove_all_choices()

    assert len(question.choices) == 0

# 3
def test_set_correct_choices_for_the_question():
    question = Question(title='q2')
    choice1 = question.add_choice('a')
    choice2 = question.add_choice('b')
    choice3 = question.add_choice('c')

    question.set_correct_choices([choice1.id, choice3.id])

    assert choice1.is_correct
    assert not choice2.is_correct
    assert choice3.is_correct

# 4
def test_added_choices_receive_sequential_ids():
    question = Question(title='q2')

    choice1 = question.add_choice('a')
    choice2 = question.add_choice('b')
    choice3 = question.add_choice('c')

    assert choice1.id == 1
    assert choice2.id == 2
    assert choice3.id == 3

# 5
def test_set_correct_choices_with_invalid_id():
    question = Question(title='q2')
    question.add_choice('a')

    with pytest.raises(Exception):
        question.set_correct_choices([999])
# 6
def test_remove_choice_with_invalid_id():
    question = Question(title='q2')
    question.add_choice('a')

    with pytest.raises(Exception):
        question.remove_choice_by_id(999)

# 7
def test_correct_selected_choices():
    question = Question(title='q2', max_selections=2)

    choice1 = question.add_choice('a', True)
    choice2 = question.add_choice('b', False)
    choice3 = question.add_choice('c', True)

    result = question.correct_selected_choices([choice1.id, choice2.id])

    assert result == [choice1.id]

# 8
def test_correct_selected_choices_without_correct_choice():
    question = Question(title='q2', max_selections=2)

    choice2 = question.add_choice('b', False)

    result = question.correct_selected_choices([choice2.id])

    assert result == []

# 9
def test_correct_selected_choices_exceeding_max_selections():
    question = Question(title='q2', max_selections=2)

    choice1 = question.add_choice('a', True)
    choice2 = question.add_choice('b', False)
    choice3 = question.add_choice('c', True)

    with pytest.raises(Exception):
        question.correct_selected_choices([choice1.id, choice2.id, choice3.id])  

# 10
def test_add_choice_with_empty_text():
    question = Question(title='q2')

    with pytest.raises(Exception):
        question.add_choice('')