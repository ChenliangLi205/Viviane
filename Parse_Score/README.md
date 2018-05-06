
to parse a musicXML file, we extract these elements：


* part-list 
	* score-part
		* part-name
* part
	* measure
		* attributes 
			* divisions
			* key
				* fifths
				* mode
			* time
				* beats
				* beat-type
			* clef
				* sign
				* line
		* **note**
			* pitch
				* step
				* alter   (if so)
				* octave
			* duration
			* type
			* stem