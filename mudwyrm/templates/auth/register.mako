<%inherit file="base.mako"/>

<%def name="header()"></%def>

<h1>${_(u"New Mudwyrm account")}</h1>

${form.begin(request.url)}
  ${form.csrf_token()}
  
  <div class="row">
    ${form.label('name', "Username:")}
    ${form.text('name', maxlength=h.MAX_STR_LENGTH, autofocus='')}
  </div>
  ${form.errorlist('name')}
  
  <div class="row">
    ${form.label('password', "Password:")}
    ${form.password('password', maxlength=h.MAX_STR_LENGTH)}
  </div>
  ${form.errorlist('password')}
  
  <div class="row">
    ${form.label('password_confirmation', "Confirm password:")}
    ${form.password('password_confirmation', maxlength=h.MAX_STR_LENGTH)}
  </div>
  ${form.errorlist('password_confirmation')}
  
  <div class="row">
    ${form.label('email', "E-mail address:")}
    ${form.text('email', maxlength=h.MAX_STR_LENGTH, type='email')}
  </div>
  ${form.errorlist('email')}
  
  <div class="lrow">
    ${form.submit('submit', "Register")}
    <a href="/">${_(u"Cancel")}</a>
  </div>
${form.end()}