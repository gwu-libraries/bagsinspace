<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" 
	xmlns:qdc="http://xxxxxx.gelman.gwu.edu/schemas/qdc/2010/09/15/"
	xmlns:marc="http://www.loc.gov/MARC21/slim"
	xmlns:dc="http://purl.org/dc/elements/1.1/"
	xmlns:dcterms="http://purl.org/dc/terms/"
	xmlns:marcrel="http://www.loc.gov/marc/relators/"
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
	
	<xsl:import href="gwu-marc-subfields.xslt"/>
	
	<xsl:output method="xml" version="1.0" encoding="UTF-8" indent="yes"/>
	
	<!-- ##################################################################### -->
	<!-- Helper template 1: outputs data from subfields determined by tag number -->
	<!-- ##################################################################### -->	
	<xsl:template name="outputSubfields">
		
		<xsl:param name="tag">
			<xsl:value-of select="./@tag"/>
		</xsl:param>
		<xsl:param name="delimiter"><xsl:text> </xsl:text></xsl:param>
		
		<!-- Retrieve selected subfields if they are not passed in -->
		<xsl:param name="codes">
			<xsl:call-template name="codeList">
				<xsl:with-param name="tag" select="$tag"/>
			</xsl:call-template>
		</xsl:param>
		
		<!-- cycle thru subfields and match against selected codes, save value of matched codes to variable -->
		<xsl:variable name="output">
			<xsl:for-each select="marc:subfield">
				<xsl:if test="contains($codes, @code)">
					<xsl:value-of select="text()"/><xsl:value-of select="$delimiter"/>
				</xsl:if>
			</xsl:for-each>
		</xsl:variable>
		
		<!-- output the subfield values -->
		<xsl:value-of select="substring($output,1,string-length($output)-string-length($delimiter))"/>

	</xsl:template>


	<!-- ##################################################################### -->
	<!-- Helper template 2: retrieves linked alternative graphic representations -->
	<!-- ##################################################################### -->	
	<xsl:template name="linkedFields">
	
		<xsl:param name="element"/>
		<xsl:param name="subelement"/>
		<xsl:param name="tag">
			<xsl:value-of select="@tag"/>
		</xsl:param>
		
		<!-- Look for a link in subfield $6 and parse it out -->
		<xsl:for-each select="marc:subfield[@code=6]">
			<xsl:variable name="linker">
				<xsl:value-of select="."/>
			</xsl:variable>
			<xsl:variable name="linktag" select="substring($linker,1,3)"/>
			<xsl:variable name="linknum" select="substring($linker, 5,2)"/>
			
			<!-- Look for the linked datafield in the record -->
			<xsl:for-each select="../../marc:datafield[@tag=$linktag]">
				<xsl:variable name="linked">
					<xsl:value-of select="marc:subfield[@code=6]"/>
				</xsl:variable>
				<xsl:variable name="matchtag" select="substring($linked,1,3)"/>
				<xsl:variable name="matchnum" select="substring($linked,5,2)"/>
					
				<!-- If a datafield matches the link call the output template -->
				<xsl:if test="$tag=$matchtag and $matchnum=$linknum">
					<xsl:element name="{$element}">
						<xsl:choose>
							<xsl:when test="string-length($subelement) &gt; 0">
								<xsl:element name="{$subelement}">
									<xsl:call-template name="outputSubfields">
										<xsl:with-param name="tag" select="$tag"/>
									</xsl:call-template>
								</xsl:element>
							</xsl:when>
							<xsl:when test="string-length($subelement) = 0 ">
								<xsl:call-template name="outputSubfields">
									<xsl:with-param name="tag" select="$tag"/>
								</xsl:call-template>
							</xsl:when>
						</xsl:choose>
					</xsl:element>
				</xsl:if>
					
			</xsl:for-each>
				
		</xsl:for-each>
		
	</xsl:template>

	<!-- ##################################################################### -->
	<!-- Helper template 3: retrieves alternative graphic representations that are not directly linked -->
	<!-- ##################################################################### -->
	<xsl:template name="unlinkedFields">
		
		<xsl:param name="element"/>
		<xsl:param name="subelement"/>
		<xsl:param name="tags"/>
		
		<!-- Look for unlinked datafields in the record and parse their links -->
		<xsl:for-each select="marc:datafield[@tag=880]">
			<xsl:variable name="linked">
				<xsl:value-of select="marc:subfield[@code=6]"/>
			</xsl:variable>
			<xsl:variable name="matchtag" select="substring($linked,1,3)"/>
			<xsl:variable name="matchnum" select="substring($linked,5,2)"/>
			
			<!-- detrmine if the datafield matches the desired tag and it is unlinked -->
			<xsl:if test="contains($tags,$matchtag) and $matchnum=00">
				<xsl:element name="{$element}">
					<xsl:choose>
						<xsl:when test="string-length($subelement) &gt; 0">
							<xsl:element name="{$subelement}">
								<xsl:call-template name="outputSubfields">
									<xsl:with-param name="tag" select="$matchtag"/>
								</xsl:call-template>
							</xsl:element>
						</xsl:when>
						<xsl:when test="string-length($subelement) = 0 ">
							<xsl:call-template name="outputSubfields">
								<xsl:with-param name="tag" select="$matchtag"/>
							</xsl:call-template>
						</xsl:when>
					</xsl:choose>
				</xsl:element>
			</xsl:if>
			
		</xsl:for-each>	
	</xsl:template>
	
	
	
	<!-- ##################################################################### -->
	<!-- Helper template 4: splits the note/title subfields in a relation datafield from the URI subfield -->
	<!-- ##################################################################### -->	
	<xsl:template name="noteUriRelation">
		<xsl:param name="noteSubfields">nt</xsl:param>
		<xsl:param name="uriSubfields">o</xsl:param>
		<xsl:param name="elementName">dcterms:isVersionOf</xsl:param>
	
		<!-- Pull note/title values -->
		<xsl:variable name="note">
			<xsl:call-template name="outputSubfields">
				<xsl:with-param name="codes">
					<xsl:value-of select="$noteSubfields"/>
				</xsl:with-param>
			</xsl:call-template>
		</xsl:variable>
		
		<!-- Pull URI value -->
		<xsl:variable name="url">
			<xsl:call-template name="outputSubfields">
				<xsl:with-param name="codes">
					<xsl:value-of select="$uriSubfields"/>
				</xsl:with-param>
			</xsl:call-template>
		</xsl:variable>
		
		<!-- Output note/title if exist -->
		<xsl:if test="string-length($note) &gt; 0">
			<xsl:element name="{$elementName}">
				<xsl:value-of select="$note"/>
			</xsl:element>
		</xsl:if>
		
		<!-- Output URI if exists -->
		<xsl:if test="string-length($url) &gt; 0">
			<xsl:element name="{$elementName}">
				<xsl:attribute name="xsi:type">dcterms:URI</xsl:attribute>
				<xsl:value-of select="$url"/>
			</xsl:element>
		</xsl:if>
		
		<xsl:call-template name="linkedFields">
			<xsl:with-param name="element" select="$elementName"/>
		</xsl:call-template>
	</xsl:template>
	
	<!-- ##################################################################### -->
	<!-- Helper template 5: fixes bad marc relator codes -->
	<!-- ##################################################################### -->
	<xsl:template name="fixMarcRel">
		<xsl:param name="relator"/>
		<xsl:choose>
			<xsl:when test="contains($relator, ' ')">
				<xsl:value-of select="substring-before($relator,' ')"/>
			</xsl:when>
			<xsl:when test="contains($relator, '.')">
				<xsl:value-of select="substring-before($relator,'.')"/>
			</xsl:when>
			<xsl:otherwise>
				<xsl:value-of select="$relator"/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>

	<!-- ##################################################################### -->
	<!-- Helper template 6: finds the volume of the current item based on barcode -->
	<!-- ##################################################################### -->
	<xsl:template name="getVolume">
		<xsl:param name="barcode"/>
		<xsl:for-each select="//marc:datafield[@tag=948]">
			<xsl:variable name="subfield-t">
				<xsl:if test="marc:subfield[@code='p'] = $barcode">
					<xsl:value-of select="marc:subfield[@code='t']"/>
				</xsl:if>
			</xsl:variable>
			<xsl:if test="string-length($subfield-t) &gt; 0">[<xsl:value-of select="$subfield-t"/>]</xsl:if>
		</xsl:for-each>
	</xsl:template>

	
</xsl:stylesheet>
