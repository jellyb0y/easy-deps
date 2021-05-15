install:
	pip install ezdeps
	ezdeps install

clean:
	rm -r build dist *.egg-info || echo 'Already cleaned'

build:
	ezdeps build

publish:
	ezdeps publish -R pypi --clear
