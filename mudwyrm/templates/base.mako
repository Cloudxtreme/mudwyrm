<%def name="stylesheet_link(name, media='screen')">
  ${h.stylesheet_link('/css/' + name, media=media)}
</%def>

<!doctype html>
<!--[if lt IE 7 ]> <html lang="en" class="no-js ie6"> <![endif]-->
<!--[if IE 7 ]>    <html lang="en" class="no-js ie7"> <![endif]-->
<!--[if IE 8 ]>    <html lang="en" class="no-js ie8"> <![endif]-->
<!--[if IE 9 ]>    <html lang="en" class="no-js ie9"> <![endif]-->
<!--[if (gt IE 9)|!(IE)]><!--> <html lang="en" class="no-js"> <!--<![endif]-->
<head>
	<meta charset="UTF-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
	
	<title>${self.title()}</title>
	<meta name="description" content="${self.description()}">
	<meta name="author" content="${self.author()}">
	
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	
	<link rel="shortcut icon" href="/favicon.ico">
	<link rel="apple-touch-icon" href="/apple-touch-icon.png">
		
	${self.stylesheets()}
	<script src="/js/libs/modernizr-1.7.min.js"></script>
</head>
<body>
	<div id="container">
		<header>${self.header()}</header>
		<div id="main" role="main">${self.main()}</div>
		<footer>${self.footer()}</footer>
	</div>
	
	${self.scripts()}
	<!--[if lt IE 7 ]>
	<script src='/js/libs/dd_belatedpng.js'></script>
	<script> DD_belatedPNG.fix('img, .png_bg');</script>
	<![endif]-->
</body>
</html>

<%def name="title()">Mudwyrm</%def>
<%def name="description()">The web-based MUD client</%def>
<%def name="author()">voidseeker</%def>

<%def name="stylesheets()">
	${self.stylesheet_link('handheld.css', 'handheld')}
</%def>

<%def name="scripts()">
	<script src="/js/libs/require.js"></script>
</%def>

<%def name="header()">
  <div>
    <a id="logo" href="/">Mudwyrm</a>
    <div id="userbar">
	  % if request.remote_user:
		Welcome, <strong>${request.remote_user}</strong>.
		<a href="/logout">Log out</a>
	  % else:
	    <a href="/login?came_from=${request.url}">Log in</a>
	  % endif
    </div>
  </div>
</%def>

<%def name="main()">
    ${next.body()}
</%def>

<%def name="footer()">
</%def>