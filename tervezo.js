highlight = function(e) {
	/**
	 * Meghatározom az egyes napokhoz tartozó oszlopok "szélességét" (colspan értékeket)
	 */
	theadChildren = document.getElementsByClassName('thead')[0].children;
	theadLens = [];
	for (i = 0; i < theadChildren.length; ++i) {
		val = parseInt(theadChildren[i].attributes['colspan'].value);
		theadLens.push(val);
	}
	/**
	 * Kattintott elem sorszámának meghatározása (pontosabban: index száma)
	 */
	parentChildren = e.parentElement.children;
	index = 0;
	while (index < parentChildren.length) {
		if (e == parentChildren[index])
			break;
		else
			++index;
		if (index == parentChildren.length)
			index = -1; //nincs tala'lat
	}
	/**
	 * Kummulálás a besoroláshoz
	 */
	theadLensKum = [];
	for (i = 0; i < theadLens.length; ++i) {
		theadLensKum[i] = theadLens[i];
		for (j = 0; j < i; ++j)
			theadLensKum[i] += theadLens[j];
	}
	/**
	 * Hét napjának indexének a meghatározása (a hét melyik napja alatt van a kattintott mező)
	 */
	theadLenIndex = 0;
	while(theadLenIndex < theadLens.length) {
		if (index < theadLensKum[theadLenIndex])
			break;
		else
			++theadLenIndex;
	}
	/**
	 * Oszlophatárok kijelölése
	 */
	b0 = 0;
	b1 = theadLensKum[theadLensKum.length-1];
	if (theadLenIndex != 0)
		b0 = theadLensKum[theadLenIndex-1];
	if (theadLenIndex != theadLens.length-1)
		b1 = theadLensKum[theadLenIndex];
	/**
	 * Kijelölt mező szélességének (colspan) módosítása, körülvevők elrejtése
	 */
	newColSpanValue = b1-b0;
	if (e.colSpan == newColSpanValue)
		newColSpanValue = 1;
	for (i = b0; i < b1; ++i) {
		current = parentChildren[i];
		if (current == e)
			current.colSpan = newColSpanValue;
		else {
			newDisplayValue = "none";
			if (current.style.display == newDisplayValue)
				newDisplayValue = "";
			current.style.display = newDisplayValue;
		}
	}
	/*
	console.log(index);
	console.log(theadLens);
	console.log(theadLensKum);
	console.log(theadLenIndex);
	console.log(b0 + " " + b1);
	*/
}