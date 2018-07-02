from flask import Flask, render_template, request, redirect, session, url_for
import configmaker
import exceptions
app = Flask(__name__)
app.secret_key = 'howdy_pardner'
config_maker = configmaker.ConfigMaker()
debug = False


@app.route('/', methods=['GET', 'POST'])
def form():
	existing_config = config_maker.existing_config
	return render_template('form.html', existing_config=existing_config)


@app.route('/success', methods=['GET', 'POST'])
def success():
	try:
		config_maker.Update_Json(request.form)
	except exceptions.ConfigError as e:
		session['error'] = str(e)
		return redirect(url_for('error'))
	except Exception as e:
		session['error'] = str(e)
		return redirect(url_for('error'))
	return render_template('success.html')


@app.route('/error')
def error():
	return render_template('error.html', error=session.get('error').split('\n'))


if __name__ == "__main__":
	if debug:
		app.run(debug=True, use_debugger=False, use_reloader=False)
	else:
		app.run(host='0.0.0.0')
