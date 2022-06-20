# from crypt import methods (this is throwing an error that is not supported on windows)
from asyncio.windows_events import NULL
import os
from tkinter.messagebox import QUESTION
from unicodedata import category
from urllib import response
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy.sql.expression import func
import random
import json

from sqlalchemy import null, true

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


#  HANDLE PAGINATION
def pagination(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page-1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = [question.format() for question in selection]
    current_question = questions[start:end]

    return current_question


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app)
    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Headers',
                             'GET, POST, PATCH, DELETE, OPTIONS')
        response.headers.add('Access-Control-Allow-Credential',
                             'true')

        return response
    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route("/categories")
    def get_categories():
        categories = Category.query.all()
        selection = {}

        if len(categories) == 0:
            abort(404)

        for cat in categories:
            selection[cat.id] = cat.type

        return jsonify({
            "Success": True,
            "categories": selection,
            "total": len(categories)

        })

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should cupdate the questions.
    """
    @app.route("/questions")
    def get_all_quetions():
        questions = Question.query.order_by(Question.id).all()
        paginated_quest = pagination(request, questions)
        categories = Category.query.all()
        selection = {}
        current_category = categories[0].format()['id']

        if len(questions) == 0:
            abort(404)
        for cat in categories:
            selection[cat.id] = cat.type

        return jsonify({
            "Success": True,
            "questions": paginated_quest,
            "categories": selection,
            "current_category": current_category,
            "total_questions": len(paginated_quest),
            "status": 200

        })
    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route("/questions/<int:id>", methods=['DELETE'])
    def delete_ques(id):
        try:
            question = Question.query.filter(Question.id == id).one_or_none()
            if question is not NULL:
                question.delete()
                return jsonify({
                    "status": 200,
                    "success": True,
                })
            else:
                abort(404)
        except:
            abort(422)
    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route("/questions/", methods=['POST'])
    def create_question():
        body = request.get_json()

        search_term = body.get('searchTerm')
        question = body.get("question")
        answer = body.get("answer")
        category = body.get("category")
        difficulty = body.get("difficulty")

        categories = Category.query.all()
        selection = {}

        for cat in categories:
            selection[cat.id] = cat.type

        try:

            if search_term:

                question = Question.query.order_by(Question.id).filter(
                    Question.question.ilike("%{}%".format(search_term)))
                paginate_question = pagination(request, question)
                print("this is the search ", search_term)
                return jsonify(
                    {
                        "success": True,
                        "status": 200,
                        "questions": paginate_question,
                        "total_books": len(paginate_question),
                        "categories": selection


                    }
                )

            else:
                question = Question(
                    question=question,
                    answer=answer,
                    category=category,
                    difficulty=difficulty
                )
                question.insert()

                questions = Question.query.all()
                paginated_quest = pagination(request, questions)

            return jsonify({
                "Success": True,
                "questions": [paginated_quest],
                "total": len(paginated_quest),
                "status": 200

            })
        except:
            abort(422)
    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    # @app.route("/questions", methods=['POST'])
    # def search_question():
    #     search_term = request.get_json.get("searchTerm", None)
    #     print("this is the search trem", search_term)
    #     query_result = Question.query.order_by(Question.id).filter(
    #         Question.question.ilike(f"{search_term}"))
    #     get_related_search = pagination(request, query_result)

    #     return jsonify(
    #         {
    #             "success": True,
    #             "questions": get_related_search,
    #             "total_books": len(query_result.all())

    #         }
    #     )

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:id>/questions')
    def get_ques_by_id(id):
        cat_id = Category.query.get(id)
        questions = Question.query.filter(Question.category == id).all()

        return jsonify({
            "success": True,
            "status": 200,
            "questions": [ques.format() for ques in questions],
            "total_questions": len(questions),

        })

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route("/quizzes", methods=["post"])
    def play_quiz():

        body = request.get_json()

        previousQuestion = body.get('previous_questions')
        category = body.get('quiz_category')

        if category['id'] == 0:
            current_question = Question.query.filter(
                Question.question != previousQuestion).order_by(func.random()).first()
        else:
            current_question = Question.query.filter(
                Question.category == category['id'] and Question.question != previousQuestion).order_by(func.random()).first()

        if not current_question:
            abort(400)

        return jsonify({
            "status": 200,
            "success": True,
            "question":  current_question.format()
        })

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404,
                    "message": "resource not found"}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422,
                    "message": "unprocessable"}),
            422,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "bad request"}), 400

    @app.errorhandler(405)
    def method_not_allowed(error):
        return (
            jsonify({"success": False, "error": 405,
                    "message": "method not allowed"}),
            405,
        )

    @app.errorhandler(500)
    def internal_server_error(error):
        return (
            jsonify({"success": False, "error": 405,
                     "message": "internal server error"}),
            500,
        )
    return app
