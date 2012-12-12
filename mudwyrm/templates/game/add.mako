<%inherit file="/base.mako"/>

<%def name="stylesheets()">
  ${self.stylesheet_link('game.css')}
  ${parent.stylesheets()}
</%def>

<h1>${_(u"Create a game")}</h1>

${form.begin(request.url)}
  ${form.csrf_token()}
  
  <div class="row">
    ${form.label('name', "Name:")}
    ${form.text('name', maxlength=h.MAX_STR_LENGTH, autofocus='', required='')}
  </div>
  ${form.errorlist('name')}
  
  <div class="row">
    ${form.label('address', "Server address:")}
    ${form.text('address', maxlength=h.MAX_STR_LENGTH, required='')}
  </div>
  ${form.errorlist('address')}
  
  <div class="row">
    ${form.label('port', "Server port:")}
    ${form.text('port', maxlength=h.MAX_STR_LENGTH, required='')}
  </div>
  ${form.errorlist('port')}
  
  <div class="lrow">
    ${form.submit('submit', "Create")}
    <a href="${request.route_url('games')}">${_(u"Cancel")}</a>
  </div>
${form.end()}