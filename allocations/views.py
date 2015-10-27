from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core import validators
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django import forms
from pytas.http import TASClient
from tas.forms import PasswordResetRequestForm, PasswordResetConfirmForm
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required, user_passes_test

import re
import logging
import json
import math
import time

logger = logging.getLogger(__name__)

def allocation_admin_or_superuser(user):
    if user:
        logger.debug( 'If user has allocation admin role: %s', user.groups.filter(name='Allocation Admin').count() )
        return (user.groups.filter(name='Allocation Admin').count() == 1) or user.is_superuser
    return False

@login_required
@user_passes_test(allocation_admin_or_superuser, login_url='/admin/allocations/denied/')
def index( request ):
    user = request.user
    logger.debug( 'Serving allocation approval view to: %s', user.username )
    context = {}
    return render(request, 'allocations/index.html', context)

def denied( request ):
    user = request.user
    if user:
        logger.debug( 'Denying allocation approval view to: %s', user.username )
    context = {}
    return render(request, 'allocations/denied.html', context)

@login_required
@user_passes_test(allocation_admin_or_superuser, login_url='/admin/allocations/denied/')
def view( request ):
    resp = ''
    try:
        tas = TASClient()
        resp = tas.projects_for_group('Chameleon')
        logger.debug( 'Total projects: %s', len(resp) )
    except Exception as e:
        logger.exception('Error loading chameleon projects')
        messages.error( request, e[0] )
        raise Exception('Error loading chameleon projects')
    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
@user_passes_test(allocation_admin_or_superuser, login_url='/admin/allocations/denied/')
def user_select( request ):
    user = request.user
    logger.debug( 'Serving user projects view to: %s', user.username )
    context = {}
    return render(request, 'allocations/user-projects.html', context)

@login_required
@user_passes_test(allocation_admin_or_superuser, login_url='/admin/allocations/denied/')
def user_projects( request, username ):
    logger.info( 'User projects requested by admin: %s for user %s', request.user, username )
    resp = []
    try:
        if username:
            tas = TASClient()
            userProjects = tas.projects_for_user( username=username )
            chameleonProjects = tas.projects_for_group('Chameleon');
            if (chameleonProjects and userProjects):
                for project in userProjects:
                    if project in chameleonProjects:
                        resp.append(project)
                        logger.info( 'Total chameleon projects for user %s: %s', username, len( resp ) )
    except Exception as e:
        logger.exception('Error loading projects for user: %s', username)
        raise Exception('Error loading projects for user: %s', username)
    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
@user_passes_test(allocation_admin_or_superuser, login_url='/admin/allocations/denied/')
def approval( request ):
    resp = {}
    errors = []
    status = ''
    if request.POST:
        tas = TASClient()
        userData = tas.get_user( username=request.user )
        data = json.loads(request.body)
        data['reviewer'] = userData['username']
        data['reviewerId'] = userData['id']
        logger.info( 'Allocation approval requested by admin: %s', request.user )
        validate_datestring = validators.RegexValidator( '^\d{4}-\d{2}-\d{2}$' )
        validate_datetimestring = validators.RegexValidator( '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$' )
        if not data['decisionSummary']:
            errors.append('Decision Summary is required.')

        if not data['status']:
            errors.append('Status is required. ')
        elif not data['status'] in ['Pending', 'pending', 'Approved', 'approved', 'Rejected', 'rejected']:
            errors.append('Status must be "Pending", "pending", "Approved", "approved", "Rejected", "rejected"')
        else:
            if data['start']:
                try:
                    validate_datestring( data['start'] )
                except ValidationError:
                    errors.append('Start date must be a valid date string e.g. "2015-05-20" .')
            elif data['status'].lower() == 'approved':
                 errors.append('Start date is required.')

            if data['end']:
                try:
                    validate_datestring( data['end'] )
                except ValidationError:
                    errors.append('Start date must be a valid date string e.g. "2015-05-20" .')
            elif data['status'].lower() == 'approved':
                 errors.append('Start date is required.')

        if data['computeAllocated']:
            try:
                data['computeAllocated'] = round(float( data['computeAllocated'] ), 2)
            except ValueError:
                errors.append('Compute Allocated must be a number.')

        if data['computeRequested']:
            try:
                data['computeRequested'] = round(float( data['computeRequested'] ), 2)
            except ValueError:
                errors.append('Compute Requested must be a number.')

        if data['storageAllocated']:
            try:
                data['storageAllocated'] = round(float( data['storageAllocated'] ), 2)
            except ValueError:
                errors.append('Storage Allocated must be a number.')

        if data['storageRequested']:
            try:
                data['storageRequested'] = round(float( data['storageRequested'] ), 2)
            except ValueError:
                errors.append('Storage Requested must be a number.')

        if data['memoryAllocated']:
            try:
                data['memoryAllocated'] = round(float( data['memoryAllocated'] ), 2)
            except ValueError:
                errors.append('Memory Allocated must be a number.')

        if data['memoryRequested']:
            try:
                data['memoryRequested'] = round(float( data['memoryRequested'] ), 2)
            except ValueError:
                errors.append('Memory Requested must be a number.')

        if data['projectId']:
            try:
                data['projectId'] = int( data['projectId'] )
            except ValueError:
                errors.append('Project id must be number.')
        else:
            errors['projectId'] = 'Project id is required.'

        if not data['project']:
            errors.append('Project charge code is required.')

        if data['reviewerId']:
            try:
                data['reviewerId'] = int( data['reviewerId'] )
            except ValueError:
                errors.append('Reviewer id must be number.')
        else:
            errors.append('Reviewer id is required.')

        if not data['reviewer']:
            errors.append('Reviewer username is required.')

        if data['dateRequested']:
            try:
                validate_datetimestring(data['dateRequested'])
            except ValidationError:
                errors.append('Requested date must be a valid date string e.g. "2015-05-20T05:00:00Z" .')
        #else:
        #     errors['dateRequested'] = 'Requested date is required.'

        if data['dateReviewed']:
            try:
                validate_datestring( data['dateReviewed'] )
            except ValidationError:
                errors.append('Reviewed date must be a valid date string e.g. "2015-05-20" .')
        else:
             errors.append('Reviewed date is required.')
        if len( errors ) == 0:
            # source
            data['source'] = 'Chameleon'

            # log the request
            logger.info( 'Request data passed validation. Calling TAS ...')
            logger.info( 'Allocation approval request data: %s', json.dumps( data ) )
            try:
                resp['result'] = tas.allocation_approval( data['id'], data )
                logger.info('Allocation approval TAS response: data=%s', json.dumps(resp['result']))
                status = 'success'
            except Exception as e:
                logger.exception('Error processing allocation approval.', e.args[1])
                status = 'error'
                errors.append(e.args[1])

        else:
            logger.info( 'Request data failed validation. %s', errors.values())
            status = 'error'

    else:
        status = 'error'
        errors.append('Only POST method allowed.')
    resp['status'] = status
    resp['messages'] = errors
    return HttpResponse(json.dumps(resp), content_type="application/json")

def allocations_template(request, resource):
    logger.debug('Template requested: %s.html', resource)
    templateUrl = 'allocations/%s.html' %resource
    return render_to_response(templateUrl)
