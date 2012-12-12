<%inherit file="/base.mako"/>

<%def name="stylesheets()">
  ${parent.stylesheets()}
  ${self.stylesheet_link('auth.css')}
</%def>

${next.body()}