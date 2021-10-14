"""
Style difflib HTML
"""
import difflib


class CustomHtmlDiff(difflib.HtmlDiff):
    """
    Overwrite templates and style
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._file_template = """
            <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
                    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
            <html>
            <head>
                <meta http-equiv="Content-Type"
                    content="text/html; charset=%(charset)s" />
                <title></title>
                <style type="text/css">%(styles)s
                </style>
                <link rel="preconnect" href="https://fonts.googleapis.com">
                <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
                <link href="https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@300;700&display=swap" rel="stylesheet"> 
            </head>
            <body>
                <div class="table">
                    %(table)s
                </div>
                <div>
                    %(legend)s
                </div>
            </body>
            </html>
        """

        self._styles = """
            :root {
              --fw-normal: 300;
              --fw-bold: 700;
              --clr-accent: 20, 147, 190;
            }

            body {
              font-size: 90%;
            }

            table.diff,
            .legend {
              font-family: 'Roboto Mono', monospace;
              font-weight: var(--fw-normal);
              border: medium;
              margin-bottom: 2rem;
              background-color: rgba(var(--clr-accent), 0.01);
              /* border-bottom: 1px solid black; */
            }

            .diff_header {
              background-color: rgba(var(--clr-accent), 0.2);
            }

            td.diff_header {
              text-align: right;
              padding: 0 0.25rem;
            }

            .diff_next {
              background-color: rgba(var(--clr-accent), 0.4);
              padding: 0 0.25rem;
            }

            .diff_next a,
            .links-legend::first-letter {
              font-size: 90%;
              font-weight: var(--fw-bold);
              text-decoration: none;
              text-transform: uppercase;
              color: rgba(var(--clr-accent), 1);
              padding: 0.075rem 0.4rem;
              /* background-color: rgba(var(--clr-accent), 1); */
              border-radius: 100vw;
              margin: 0 0.3rem;
              outline: 2px solid rgba(var(--clr-accent), 1);
            }

            .diff_add {
              color: #fff;
              background-color: #479409;
              padding: 0 1rem 0 0.5rem;
            }

            .diff_chg {
              font-weight: var(--fw-bold);
              background-color: gold;
            }

            .diff_sub {
              color: #fff;
              background-color: #CD3602;
              padding: 0 1rem 0 0.5rem;
            }

            thead .diff_header {
              font-weight: var(--fw-bold);            
              padding: 1rem 0;
            }

            td[nowrap] {
              padding-left: 0.5rem;
            }

            .colors,
            .links {
              border-width: 0;
              border-style: none;
            }

            .links {
              padding-left: 0.5rem;
            }

            .legend td[class] {
              text-align: center;
            }

            .links-legend {
              text-align: left !important;              
            }

            .links-legend::first-letter {
              margin: 0;
              font-size: 80%;
              border: 2px solid rgba(var(--clr-accent), 1);
            }

        """

        self._table_template = """
            <table class="diff" id="difflib_chg_%(prefix)s_top"
                  cellspacing="0" cellpadding="0" rules="groups" >
                <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup>
                <colgroup></colgroup> <colgroup></colgroup> <colgroup></colgroup>
                %(header_row)s
                <tbody>
                    %(data_rows)s
                </tbody>
            </table>
        """

        self._legend = """
            <table class="legend" summary="Legends">
                <tr><th class="legends-th" colspan="2">Legends</th></tr>
                <tr><td><table class="colors" summary="Colors">
                              <tr><th>Colors</th> </tr>
                              <tr><td class="diff_add">Added</td></tr>
                              <tr><td class="diff_chg">Changed</td></tr>
                              <tr><td class="diff_sub">Deleted</td></tr>
                          </table></td>

                    <td><table class="links" summary="Links">
                              <tr><th colspan="2">Links</th></tr>
                              <tr><td class="links-legend">First change</td></tr>
                              <tr><td class="links-legend">Next change</td></tr>
                              <tr><td class="links-legend">Top</td></tr>
                          </table></td>
                          
                          </tr>
            </table>
        """
