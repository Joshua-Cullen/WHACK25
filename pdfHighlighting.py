import pymupdf  # import package PyMuPDF
from typing import Iterable


def highlight_pdf(input_path: str, output_path: str, phrases: Iterable[str]):
    """Open a PDF at input_path, highlight every occurrence of each phrase
    in `phrases`, and save the resulting PDF to output_path.

    - phrases: iterable of strings to search for. Each phrase is searched
      literally (case-sensitive). Callers can pre-process phrases if they
      want case-insensitive matching.
    """
    if phrases is None:
        phrases = []

    # open input PDF
    doc = pymupdf.open(input_path)

    # use a single color for highlights (yellow) so the UI is consistent
    highlight_color = pymupdf.pdfcolor["yellow"]

    for page in doc:
        for phrase in phrases:
            if not phrase or not phrase.strip():
                continue
            try:
                rects = page.search_for(phrase)
            except Exception:
                # search_for can raise on malformed input; skip problematic phrase
                rects = []

            for rect in rects:
                annot = page.add_highlight_annot(rect)
                try:
                    annot.set_colors(stroke=highlight_color)
                except Exception:
                    # older/newer pymupdf versions may differ; ignore color errors
                    pass
                annot.update()

    # save the document with these changes
    doc.save(output_path)


if __name__ == "__main__":
    # quick manual test when run directly
    highlight_pdf("mortgage_agreement_1.pdf", "output.pdf", [
        "Lender may assign or transfer this Mortgage or the Note without the consent of B",
        "For purposes of this Agreement, the follow",
        "All disputes arising out of or relating to this Agreement shall be resolved by binding arbitration in accordance with the rules of the American Arbitration Association to be conducted in Wilmington, Delaware. The decision of the arbitrator shall be final and binding. (b) Notwithstanding the foreg",
    ])