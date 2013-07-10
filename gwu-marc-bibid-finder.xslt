<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:marc="http://www.loc.gov/MARC21/slim">
	<xsl:output method="text" version="1.0" encoding="UTF-8" indent="no" />
	
	<xsl:param name="barcode"/>
	
	<xsl:template match="/">bibid=<xsl:value-of select="//marc:controlfield[@tag=001]"/>
		<xsl:call-template name="volume"/>
	</xsl:template>
	
	<xsl:template name="volume">
		<xsl:for-each select="//marc:datafield[@tag=948]">
			<xsl:if test="marc:subfield[@code='p'] = $barcode">
volume=<xsl:value-of select="marc:subfield[@code='t']"/></xsl:if>
		</xsl:for-each>
	</xsl:template>
	
	</xsl:stylesheet>
