<%inherit file="/base.mako"/>

<%def name="stylesheets()">
  ${self.stylesheet_link('game.css')}
  ${parent.stylesheets()}
</%def>

<%def name="scripts()">
  ${parent.scripts()}
</%def>

<section id="gamelist">
  <header>
    % if games:
      <h1>${_("Select a game:")}</h1>
    % else:
      <h1>${_("There are no saved games.")}</h1>
    % endif
    ${h.link_to("add", 'add', class_='control')}
  </header>
  % if games:
    <menu>
      % for game in games:
        <li>
          ${h.link_to(game.capitalize(), 'play/%s' % game, class_='game')}
          ${h.link_to("delete", 'delete/%s' % game, class_='control')}
          ${h.link_to("edit", 'edit/%s' % game, class_='control')}
        </li>
      % endfor
    </menu>
  % endif
</section>