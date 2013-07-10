<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" 
	xmlns:qdc="http://xxxxxx.gelman.gwu.edu/schemas/qdc/2010/09/15/"
	xmlns:dc="http://purl.org/dc/elements/1.1/"
	xmlns:dcterms="http://purl.org/dc/terms/"
	xmlns:marcrel="http://www.loc.gov/marc/relators/"
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
	
	<xsl:output method="xml" version="1.0" encoding="UTF-8" indent="yes" omit-xml-declaration="yes"/>
	
	<!-- ##################################################################### -->
	<!-- variables for transforming alphabetic case -->
	<!-- ##################################################################### -->
	<xsl:variable name="lowercase" select="'abcdefghijklmnopqrstuvwxyz'" />
	<xsl:variable name="uppercase" select="'ABCDEFGHIJKLMNOPQRSTUVWXYZ'" />

	
	<!-- ##################################################################### -->
	<!-- Root template. -->
	<!-- ##################################################################### -->
	<!-- Test if the input document contains a single DC record or a collection of them -->
	<xsl:template match="/">
		<xsl:for-each select="//qdc:qualifieddc">
			<dublin_core>
				<xsl:apply-templates select="."/>
			</dublin_core>
		</xsl:for-each>
	</xsl:template>
	
	<!-- ##################################################################### -->
	<!-- Main template - matches qdc:qualifieddc. -->
	<!-- ##################################################################### -->
	<xsl:template match="qdc:qualifieddc">
		
		
		<!-- STEP 1: TITLES AND ALTERNATIE TITLES -->
		<xsl:for-each select="dc:title">
			<dcvalue element="title" qualifier="none">
				<xsl:value-of select="."/>
			</dcvalue>
		</xsl:for-each>
		
		<xsl:for-each select="dcterms:alternative">
			<dcvalue element="title" qualifier="alternative">
				<xsl:value-of select="."/>
			</dcvalue>
		</xsl:for-each>
		
		<!-- STEP 2: CONTRIBUTORS -->
		<xsl:for-each select="dc:contributor">
			<dcvalue element="contributor">
				<xsl:attribute name="qualifier">
					<xsl:call-template name="getRelator"/>
				</xsl:attribute>
				<xsl:value-of select="."/>
			</dcvalue>
		</xsl:for-each>
		
		<!-- STEP 3: SUBJECT -->
		<xsl:for-each select="dc:subject">
			<dcvalue element="subject">
				<xsl:attribute name="qualifier">
					<xsl:value-of select="translate(substring(@xsi:type,9),$uppercase,$lowercase)"/>
				</xsl:attribute>
				<xsl:value-of select="."/>
			</dcvalue>
		</xsl:for-each>
		
		
		<!-- STEP 4: DESCRIPTION -->
		<xsl:for-each select="dcterms:tableOfContents">
			<dcvalue element="description" qualifier="tableofcontents">
				<xsl:value-of select="."/>
			</dcvalue>
		</xsl:for-each>
		
		<xsl:for-each select="dcterms:abstract">
			<dcvalue element="description" qualifier="abstract">
				<xsl:value-of select="."/>
			</dcvalue>
		</xsl:for-each>
		
		<xsl:for-each select="dcterms:provenance">
			<dcvalue element="description" qualifier="provenance">
				<xsl:value-of select="."/>
			</dcvalue>
		</xsl:for-each>
		
		<xsl:for-each select="dc:description">
			<dcvalue element="description" qualifier="none">
				<xsl:value-of select="."/>
			</dcvalue>
		</xsl:for-each>
		
		
		<!-- STEP 5: LANGUAGE -->
		<xsl:for-each select="dc:language">
			<dcvalue element="language">
				<xsl:attribute name="qualifier">
					<xsl:value-of select="translate(substring(@xsi:type,9),$uppercase,$lowercase)"/>
				</xsl:attribute>
				<xsl:value-of select="."/>
			</dcvalue>
		</xsl:for-each>

		<!-- STEP 6: PUBLISHER -->
		<xsl:for-each select="dc:publisher">
			<dcvalue element="publisher" qualifier="none">
				<xsl:value-of select="."/>
			</dcvalue>
		</xsl:for-each>
		
		<!--STEP 7: DATE -->
		<xsl:for-each select="dcterms:created">
			<dcvalue element="date" qualifier="created">
				<xsl:value-of select="."/>
			</dcvalue>
		</xsl:for-each>
		
		<xsl:for-each select="dcterms:issued">
			<dcvalue element="date" qualifier="issued">
				<xsl:value-of select="."/>
			</dcvalue>
		</xsl:for-each>
		
		<xsl:for-each select="dcterms:copyrighted">
			<dcvalue element="date" qualifier="copyrighted">
				<xsl:value-of select="."/>
			</dcvalue>
		</xsl:for-each>
		
		<xsl:for-each select="dcterms:modified">
			<dcvalue element="date" qualifier="modified">
				<xsl:value-of select="."/>
			</dcvalue>
		</xsl:for-each>
		
		<xsl:for-each select="dcterms:valid">
			<dcvalue element="date" qualifier="valid">
				<xsl:value-of select="."/>
			</dcvalue>
		</xsl:for-each>
		
		<xsl:for-each select="dc:date">
			<dcvalue element="date" qualifier="none">
				<xsl:value-of select="."/>
			</dcvalue>
		</xsl:for-each>
		
		
		<!-- STEP 8: TYPE -->
		<xsl:for-each select="dc:type">
			<dcvalue element="type" qualifier="none">
				<xsl:value-of select="."/>
			</dcvalue>
		</xsl:for-each>
		
		<!-- STEP 9: FORMAT -->
		<xsl:for-each select="dc:format">
			<dcvalue element="format">
				<xsl:attribute name="qualifier">
					<xsl:value-of select="translate(substring(@xsi:type,9),$uppercase,$lowercase)"/>
				</xsl:attribute>
				<xsl:value-of select="."/>
			</dcvalue>
		</xsl:for-each>
		
		<xsl:for-each select="dcterms:extent">
			<dcvalue element="format" qualifier="extent">
				<xsl:value-of select="."/>
			</dcvalue>
		</xsl:for-each>
		
		<xsl:for-each select="dcterms:medium">
			<dcvalue element="format" qualifier="medium">
				<xsl:value-of select="."/>
			</dcvalue>
		</xsl:for-each>
		
		<!-- STEP 10: IDENTIFIER -->
		<xsl:for-each select="dc:identifier">
			<xsl:choose>
				<xsl:when test="starts-with(.,'http://library.georgetown.edu')"/>
				<xsl:otherwise>
					<dcvalue element="identifier">
						<xsl:choose>
							<xsl:when test="@xsi:type">
								<xsl:attribute name="qualifier">
									<xsl:value-of select="translate(substring(@xsi:type,9),$uppercase,$lowercase)"/>
								</xsl:attribute>	
								<xsl:value-of select="."/>
							</xsl:when>		
							<xsl:when test="starts-with(text(),'ISBN')">		
								<xsl:attribute name="qualifier">isbn</xsl:attribute>
								<xsl:value-of select="substring(text(),6)"/>
							</xsl:when>
							<xsl:when test="starts-with(text(),'ISSN')">		
								<xsl:attribute name="qualifier">issn</xsl:attribute>
								<xsl:value-of select="substring(text(),6)"/>
							</xsl:when>
							<xsl:otherwise>
								<xsl:value-of select="."/>
							</xsl:otherwise>
						</xsl:choose>
					</dcvalue>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:for-each>
		
		
		<!-- STEP 11: RELATION -->
		<xsl:for-each select="dcterms:hasFormat">
			<dcvalue element="relation" qualifier="hasformat">
				<xsl:value-of select="."/>
			</dcvalue>
		</xsl:for-each>
		
		<xsl:for-each select="dcterms:hasPart">
			<dcvalue element="relation" qualifier="haspart">
				<xsl:value-of select="."/>
			</dcvalue>
		</xsl:for-each>
		
		<xsl:for-each select="dcterms:hasVersion">
			<dcvalue element="relation" qualifier="hasversion">
				<xsl:value-of select="."/>
			</dcvalue>
		</xsl:for-each>
		
		<xsl:for-each select="dcterms:isFormatOf">
			<dcvalue element="relation" qualifier="isformatof">
				<xsl:value-of select="."/>
			</dcvalue>
		</xsl:for-each>
		
		<xsl:for-each select="dcterms:isPartOf">
			<dcvalue element="relation" qualifier="ispartof">
				<xsl:value-of select="."/>
			</dcvalue>
		</xsl:for-each>
		
		<xsl:for-each select="dcterms:isReferencedBy">
			<dcvalue element="relation" qualifier="isreferencedby">
				<xsl:value-of select="."/>
			</dcvalue>
		</xsl:for-each>
		
		<xsl:for-each select="dcterms:isReplacedBy">
			<dcvalue element="relation" qualifier="isreplacedby">
				<xsl:value-of select="."/>
			</dcvalue>
		</xsl:for-each>
		
		<xsl:for-each select="dcterms:isVersionOf">
			<dcvalue element="relation" qualifier="isversionof">
				<xsl:value-of select="."/>
			</dcvalue>
		</xsl:for-each>
		
		<xsl:for-each select="dcterms:replaces">
			<dcvalue element="relation" qualifier="replaces">
				<xsl:value-of select="."/>
			</dcvalue>
		</xsl:for-each>
		
		<xsl:for-each select="dcterms:requires">
			<dcvalue element="relation" qualifier="requires">
				<xsl:value-of select="."/>
			</dcvalue>
		</xsl:for-each>
		
		<xsl:for-each select="dc:relation">
			<dcvalue element="relation" qualifier="none">
				<xsl:value-of select="."/>
			</dcvalue>
		</xsl:for-each>
		
		
		<!-- STEP 12: COVERAGE -->
		<xsl:for-each select="dcterms:spatial">
			<dcvalue element="coverage" qualifier="spatial">
				<xsl:choose>
					<xsl:when test="string-length(@xsi:type) &gt; 0">
						<xsl:value-of select="concat(translate(substring(@xsi:type,9),$uppercase,$lowercase),' ',text())"/>
					</xsl:when>
					<xsl:otherwise>
						<xsl:value-of select="."/>
					</xsl:otherwise>
				</xsl:choose>
			</dcvalue>
		</xsl:for-each>
		
		<xsl:for-each select="dcterms:temporal">
			<dcvalue element="coverage" qualifier="temporal">
				<xsl:value-of select="."/>
			</dcvalue>
		</xsl:for-each>
		
		<xsl:for-each select="dc:coverage">
			<dcvalue element="coverage" qualifier="none">
				<xsl:value-of select="."/>
			</dcvalue>
		</xsl:for-each>
		
		
		<!-- STEP 13: AUDIENCE -->
		<xsl:for-each select="dcterms:audience">
			<dcvalue element="audience" qualifier="none">
				<xsl:value-of select="."/>
			</dcvalue>
		</xsl:for-each>
		
		
		<!-- STEP 14: ACCRUAL METHOD AND PERIODICITY -->
		<xsl:for-each select="dcterms:accrualMethod">
			<dcvalue element="accrualmethod" qualifier="none">
				<xsl:value-of select="."/>
			</dcvalue>
		</xsl:for-each>
		
		<xsl:for-each select="dcterms:accrualPeriodicity">
			<dcvalue element="accrualperiodicity" qualifier="none">
				<xsl:value-of select="."/>
			</dcvalue>
		</xsl:for-each>
		
		
		<!-- STEP 15: PROVENANCE -->
		<xsl:for-each select="dcterms:provenance">
			<dcvalue element="provenance" qualifier="none">
				<xsl:value-of select="."/>
			</dcvalue>
		</xsl:for-each>
		
		
		<!-- STEP 16: SOURCE -->
		<xsl:for-each select="dc:source">
			<dcvalue element="source">
				<xsl:attribute name="qualifier">
					<xsl:value-of select="translate(substring(@xsi:type,9),$uppercase,$lowercase)"/>
				</xsl:attribute>
				<xsl:value-of select="."/>
			</dcvalue>
		</xsl:for-each>
		
		
		<!-- STEP 17: RIGHTS -->
		<xsl:for-each select="dcterms:accessRights">
			<dcvalue element="rights">
				<xsl:attribute name="qualifier">
					<xsl:choose>
						<xsl:when test="string-length(@xsi:type) &gt; 0">
							<xsl:value-of select="translate(substring(@xsi:type,9),$uppercase,$lowercase)"/>
						</xsl:when>
						<xsl:otherwise>
							access
						</xsl:otherwise>
					</xsl:choose>
				</xsl:attribute>
				<xsl:value-of select="."/>
			</dcvalue>
		</xsl:for-each>
		
		<xsl:for-each select="dcterms:rightsHolder">
			<dcvalue element="rights">
				<xsl:attribute name="qualifier">
					<xsl:choose>
						<xsl:when test="string-length(@xsi:type) &gt; 0">
							<xsl:value-of select="translate(substring(@xsi:type,9),$uppercase,$lowercase)"/>
						</xsl:when>
						<xsl:otherwise>
							holder
						</xsl:otherwise>
					</xsl:choose>
				</xsl:attribute>
				<xsl:value-of select="."/>
			</dcvalue>
		</xsl:for-each>
		
		<xsl:for-each select="dc:rights">
			<dcvalue element="rights" qualifier="none">
				<xsl:value-of select="."/>
			</dcvalue>
		</xsl:for-each>


		<!-- STEP 18: CREATOR -->
		<xsl:for-each select="dc:creator">
			<dcvalue element="creator" qualifier="none">
				<xsl:value-of select="."/>
			</dcvalue>
		</xsl:for-each>
		
		
	</xsl:template>
	
	<!-- ##################################################################### -->
	<!-- Helper template 1a. This detrmines if a contributor element is qualified with a MARC relator element and returns the appropriate value -->
	<!-- ##################################################################### -->
	<xsl:template name="getRelator">
		<xsl:choose>
			<xsl:when test="substring(name(child::node()),1,8)='marcrel:'">
				<xsl:call-template name="relatorList"/>
			</xsl:when>
			<xsl:otherwise>none</xsl:otherwise>
		</xsl:choose>		
	</xsl:template>
	
	<!-- ##################################################################### -->
	<!-- Helper template 1b. This is a mapping of MARC relator codes to DSpace qualifier values -->
	<!-- ##################################################################### -->
	<xsl:template name="relatorList">
		<xsl:param name="code">
			<xsl:value-of select="substring(name(child::node()),9)"/>
		</xsl:param>
		<xsl:choose>
			<xsl:when test="$code='aut'">author</xsl:when>
			<xsl:when test="$code='ed.'">editor</xsl:when>
			<xsl:when test="$code='edt'">editor</xsl:when>
			<xsl:when test="$code='ill'">illustrator</xsl:when>
			<xsl:otherwise>other</xsl:otherwise>
		</xsl:choose>		
	</xsl:template>
	
</xsl:stylesheet>
