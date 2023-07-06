class GetSerializerClassMixin(object):
    def get_serializer_class(self):
        """
        Returns the serializer class based on the current action and
         user's role.
         It checks serializer_role_action_classes for serializers
          dependent on role and action both. If there are no such
          serializers, it checks serializer_action_classes for
          serializers dependent only on action. If there are also no
          such serializers, it returns default serializer
          by get_serializer_class()

        """
        if hasattr(self.request.user, 'role'):
            serializer = self.serializer_role_action_classes.get(
                (self.request.user.role, self.action)
            )
            if serializer:
                return serializer

        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super(GetSerializerClassMixin, self).get_serializer_class()
