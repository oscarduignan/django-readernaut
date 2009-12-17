=================
django-readernaut
=================

Django application which provides a template tag interface to the pyreadernaut 
package. Allow's you to retrieve a Readernaut user's books.

------------
Installation
------------

You can install by running the following command inside this directory.
    
    python setup.py install

You can also install using either ``easy_install`` or ``pip``.
    
    easy_install django-readernaut
    
    pip install django-readernaut

Or you can just place the djangonaut package somewhere on your python path.

--------------
Usage Examples
--------------

First you need to add djangonaut to your INSTALLED_APPS setting.

Then you need to load the djangonaut library in any template you want to use 
this with.

    {% load djangonaut %}

This example gets a list of all books belonging to 'oscarduignan':
    
    {% get_books for "oscarduignan" as book_list %}
    
This example shows how you the other options you can pass in:

    {% get_books for "oscarduignan" from "reading" order "modified" as book_list %}

``order`` defaults to ``"-created"`` (newest books first), and ``from`` defaults 
to ``""`` (gets all books).

Note, there are no tags for retrieving user notes or contacts. If that is 
something you need, take a look at the pyreadernaut library for functions which
you can use to ease development of your note and contact template tags.

Readernaut API documentation
(http://groups.google.com/group/readernaut-api/web/restful-api-overview)
