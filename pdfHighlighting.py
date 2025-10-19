import pymupdf  # import package PyMuPDF


# open input PDF 
doc=pymupdf.open("mortgage_agreement_1.pdf")
searchingStrings = [("""Lender may assign or transfer this Mortgage or the Note without the consent of B""", 1),
                    ("""For purposes of this Agreement, the follow""", 2),
                    ("""All disputes arising out of or relating to this Agreement shall be resolved by binding arbitration in accordance with the rules of the American Arbitration Association to be conducted in Wilmington, Delaware. The decision of the arbitrator shall be final and binding. (b) Notwithstanding the foreg""", 3)]

colours = {
    1 : pymupdf.pdfcolor["green"],
    2 : pymupdf.pdfcolor["yellow"],
    3 : pymupdf.pdfcolor["red"],
}

for page in doc:
    for search in searchingStrings:
        # search for "whale", results in a list of rectangles
        rects = page.search_for(search[0])

        # highlight each found rectangle individually
        for rect in rects:
            # highlight just this specific rectangle
            annot = page.add_highlight_annot(rect)
            annot.set_colors(stroke=colours[search[1]])
            annot.update() 


# save the document with these changes
doc.save("output.pdf")