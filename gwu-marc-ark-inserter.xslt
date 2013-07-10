<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:marc="http://www.loc.gov/MARC21/slim">
	<xsl:output method="xml" version="1.0" encoding="UTF-8" indent="yes"/>
	
	<xsl:param name="ark"/>
	
	<!-- Output all elements verbatim -->
	<xsl:template match="*">
		<xsl:element name="{name()}" namespace="http://www.loc.gov/MARC21/slim">
			<xsl:apply-templates select="@*"/>
			<xsl:apply-templates/>
		</xsl:element>
  </xsl:template>

	<!-- and all attributes -->
	<xsl:template match="@*">
		<xsl:attribute name="{name()}" namespace="">
			<xsl:value-of select="."/>
		</xsl:attribute>
	</xsl:template>
	
	<!-- insert ark in an 856 field and add an 852 as well -->
	<xsl:template match="marc:datafield[@tag &gt; 856 and preceding-sibling::*[1]/@tag &lt; 856]">
		<xsl:variable name="prev-tag" select="preceding-sibling::*[1]/@tag"/>
		<!-- insert 852 -->
		<xsl:element name="datafield" namespace="http://www.loc.gov/MARC21/slim">
			<xsl:attribute name="tag" namespace="">852</xsl:attribute>
			<xsl:attribute name="ind1" namespace="">8</xsl:attribute>
			<xsl:attribute name="ind2" namespace=""><xsl:text> </xsl:text></xsl:attribute>
			<xsl:element name="subfield" namespace="http://www.loc.gov/MARC21/slim">
				<xsl:attribute name="code">b</xsl:attribute>gwg ei</xsl:element>
			<xsl:element name="subfield" namespace="http://www.loc.gov/MARC21/slim">
				<xsl:attribute name="code">h</xsl:attribute>GW: Electronic Book.</xsl:element>
		</xsl:element>		
		<!-- insert 856 -->
		<xsl:element name="datafield" namespace="http://www.loc.gov/MARC21/slim">
			<xsl:attribute name="tag" namespace="">856</xsl:attribute>
			<xsl:attribute name="ind1" namespace="">4</xsl:attribute>
			<xsl:attribute name="ind2" namespace="">1</xsl:attribute>
			<xsl:element name="subfield" namespace="http://www.loc.gov/MARC21/slim">
				<xsl:attribute name="code">u</xsl:attribute><xsl:value-of select="$ark"/></xsl:element>
			<xsl:element name="subfield" namespace="http://www.loc.gov/MARC21/slim">
				<xsl:attribute name="code">z</xsl:attribute>Click here to access.</xsl:element>
		</xsl:element>
		
		<xsl:element name="{name()}" namespace="http://www.loc.gov/MARC21/slim">
			<xsl:apply-templates select="@*"/>
			<xsl:apply-templates/>
		</xsl:element>
	</xsl:template>

</xsl:stylesheet>
