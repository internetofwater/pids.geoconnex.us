<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:s="http://www.sitemaps.org/schemas/sitemap/0.9">

<xsl:output method="html" encoding="UTF-8" indent="yes"/>

<xsl:template match="/">
<html>
<head>
  <title>geoconnex.us Sitemap</title>
  <style>
    body {
      font-family: system-ui, sans-serif;
      max-width: 900px;
      margin: 2em auto;
      line-height: 1.5;
      color: #333;
    }
    h1 {
      font-size: 1.8em;
      margin-bottom: 0.5em;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 1em;
    }
    th, td {
      border-bottom: 1px solid #ddd;
      padding: 8px 10px;
      text-align: left;
      vertical-align: top;
    }
    th {
      background: #f8f8f8;
      font-weight: 600;
      cursor: pointer;
    }
    th:hover {
      background: #eef5ff;
    }
    tr:hover td {
      background: #f3f9ff;
    }
    a {
      color: #0066cc;
      text-decoration: none;
      word-break: break-all;
    }
    a:hover {
      text-decoration: underline;
    }
    footer {
      margin-top: 2em;
      font-size: 0.9em;
      color: #777;
    }
  </style>
  <script>
    document.addEventListener('DOMContentLoaded', function() {
      document.querySelectorAll('th').forEach(th => {
        th.addEventListener('click', () => {
          const table = th.closest('table');
          const tbody = table.querySelector('tbody');
          const index = Array.from(th.parentNode.children).indexOf(th);
          const ascending = !th.classList.contains('asc');
          Array.from(table.querySelectorAll('th')).forEach(t => t.classList.remove('asc', 'desc'));
          th.classList.toggle('asc', ascending);
          th.classList.toggle('desc', !ascending);
          Array.from(tbody.querySelectorAll('tr'))
            .sort((a, b) => {
              const tA = a.children[index].innerText.trim().toLowerCase();
              const tB = b.children[index].innerText.trim().toLowerCase();
              return ascending ? tA.localeCompare(tB) : tB.localeCompare(tA);
            })
            .forEach(tr => tbody.appendChild(tr));
        });
      });
    });
  </script>
</head>
<body>

  <h1>geoconnex.us Sitemap Index</h1>
  <p>This index references <xsl:value-of select="count(s:sitemapindex/s:sitemap)"/> sitemap files.</p>
  <table>
    <thead>
      <tr>
        <th>Organization</th>
        <th>File</th>
        <th>Last Modified</th>
      </tr>
    </thead>
    <tbody>
      <xsl:for-each select="s:sitemapindex/s:sitemap">
        <xsl:variable name="full" select="s:loc"/>
        <!-- Strip https://geoconnex.us/sitemap/ -->
        <xsl:variable name="trimmed" select="substring-after($full, 'https://geoconnex.us/sitemap/')"/>
        <xsl:variable name="org" select="substring-before($trimmed, '/')"/>
        <xsl:variable name="file" select="substring-after($trimmed, '/')"/>

        <tr>
          <td><xsl:value-of select="$org"/></td>
          <td><a href="{$full}"><xsl:value-of select="$file"/></a></td>
          <td><xsl:value-of select="s:lastmod"/></td>
        </tr>
      </xsl:for-each>
    </tbody>
  </table>
</body>
</html>
</xsl:template>
</xsl:stylesheet>