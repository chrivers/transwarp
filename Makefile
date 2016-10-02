SHELL=/bin/zsh

clean:
	@./setup.py clean -a
	@rm -fv **/*~(N)
	@rm -rf **/__pycache__(N)
	@rm -rfv transwarp.egg-info
	@rm -rfv dist/
