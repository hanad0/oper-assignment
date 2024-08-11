from rest_framework import permissions

from quiz.const.user_groups import QUIZ_CREATOR, QUIZ_PARTICIPANT


class IsQuizCreator(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name=QUIZ_CREATOR).exists()


class IsQuizParticipant(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name=QUIZ_PARTICIPANT).exists()
