<%inherit file="base.mako"/>

<%def name="header()"></%def>

<h1>${_(u"Welcome to Mudwyrm")}</h1>

${form.begin(request.url)}
  ${form.csrf_token()}
  <div class="row">
    ${form.label('name', "Username:")}
    ${form.text('name', maxlength=h.MAX_STR_LENGTH, autofocus='', tabindex=1)}
  </div>
  ${form.errorlist('name')}
  <div class="row">
    ${form.label('password', "Password:")}
    ${form.password('password', maxlength=h.MAX_STR_LENGTH, tabindex=2)}
  </div>
  ${form.errorlist('password')}
  <div class="row">
    ${form.submit('submit', "Log in", tabindex=4)}
    <div class="checkbox">
      ${form.checkbox('remember', tabindex=3)}
      ${form.label('remember', "Remember me")}
    </div>
  </div>
  % if auth_failed:
    <p class="error">${_("Invalid username or password.")}</p>
  % endif
  <hr/>
  <a href="/register">${_(u"Register")}</a>
  <br/>
  <a href="/password_recovery">${_(u"Recover password")}</a>
${form.end()}
