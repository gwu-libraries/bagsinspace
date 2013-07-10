<?xml version="1.0" encoding="UTF-8"?>

<!-- 

CREATED BY: Joshua Gomez, Gelman Library, George Washington University
CREATED ON: 2010-09-15

This stylesheet converts MARCXML to qualified Dublin Core based on the mappings suggested by the Library of Congress in http://www.loc.gov/marc/marc2dc.html. Because the mapping describes a subset of the datafields, not all fields in the MARCXML are represented in the output.

This stylesheet is based on another found at http://imlsdcc.grainger.uiuc.edu/docs/stylesheets/GeneralMARCtoQDC.xsl. The current stylesheet improves upon the other in the following ways:

1. By adding functionality for retrieving linked datafields that provide alternative graphic representations of a source datafield.  For instance a 245 field may have a transliteration of a foreign language and the subfield $6 will provide a link to an 880 field which has the unicode representation of the original language's script (such as Arabic, Hebrew, Chinese, etc.) This stylesheet will retrieve both entries and produce a <dc:title> element for each.

2. Making adjustment of subfield selection easier and separate from the main stylesheet. For most of the datafield mappings, the LOC document does not specify which subfields should be included in the output. Thus, the selection of subfields for export will be a local decision. To make the decision making process easier to implement, this stylesheet imports another stylesheet, gwu-marc-subfields.xslt, which contains a template for selecting subfields based on the datafield tag.  This other stylesheet is easy to read and edit.The separation of the stylesheet logic from the policy-based subfield selction enables easier local customization.

3. Usage of the <dcterms:contributor> tag instead of the <dc:creator> tag, which the LOC and DCMI advise against using.

4a. Refinement of the <dcterms:contributor> tag with MARC relator codes.  The MARC relator codes are used to specify the relationship of a contributor to the work, such as 'author', 'director', 'editor', etc. These can be taken from subfield $e of a main entry (100 field) or other fields such as: 110,111,700,710,711,720. In the output document, these appear like:  

<dcterms:contributor>
	<marcrel:aut>Twain, Mark</marcrel:aut>
</dcterms:contributor>

4b. Additionally, as many MARC records do not have the 100 $e filled out, this stylesheet allows for locally based assumptions about the main entry. For instance, in the project for which this stylesheet was created, we are processing only books, and it is fairly safe for us to assume that the main entry can be described as author, so when calling this stylesheet we pass that parameter as our assumption. This can be changed based on local usage. For example, if one were to use this styelsheet for processing musical CD metadata only, than it may be safe to assume that the main entry is a musician, <marcrel:mus>. Be awar that this can be a dangerous assumption and should only be used for small collections of items which are known to conform to the assumption.

The purpose of making this dangerous assumption was for improving the metadata for items ingested into a DSpace repository. Without the assumption of 'author' for the main entry, our collection of books would all appear with only generic 'contributor' elements in the user interface. 

-->

<!-- TODO: determine URL for gw-qdc schema/namespace -->
<xsl:stylesheet version="1.0" 
	xmlns:qdc="http://xxxxxx.gelman.gwu.edu/schemas/qdc/2010/09/15/"
	xmlns:marc="http://www.loc.gov/MARC21/slim"
	xmlns:dc="http://purl.org/dc/elements/1.1/"
	xmlns:dcterms="http://purl.org/dc/terms/"
	xmlns:marcrel="http://www.loc.gov/marc/relators/"
	xmlns:xsl="http://www.w3.org/1999/XSL/Transform" 
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
	
	<xsl:import href="gwu-marc-to-qdc-helper.xslt"/>
	
	<xsl:output method="xml" version="1.0" encoding="UTF-8" indent="yes"/>
	
	
	<!-- 
	WARNING!!! The following parameter is used to make an assumption about the relation of a main entry to the work.  Use the MARC relator codes (see: http://www.loc.gov/marc/relators/) as values for the parameter. For example, if you are scanning books and plan to convert MARC records to DC and know that the main entries in your MARC records are authors, then pass 'aut' as an assumption. If you are unsure about the relation for ALL of your records, DO NOT pass in an assumption parameter. 
	
	The purpose of this assumption is to distinguish the main entry author from other contributors. Without the assumption all contributors could be listed in generic <dc:contributor> elements. This script looks for MARC relator terms in subfield $e of the MARC contributor fields to create qualified elements, but this subfield is rarely used, so this parameter is introduced as a method to make an assumption about the main entry. 	
	-->
	<xsl:param name="assumption"/>
	
	<xsl:param name="barcode"/>
	
	<!-- ##################################################################### -->
	<!-- Root template. -->
	<!-- ##################################################################### -->
	<!-- Test if the input document contains a single MARC record or a collection of them -->
	<xsl:template match="/">
		<xsl:if test="marc:collection">
			<!-- TODO: create GWU-QDC schema and detrmine URL for it -->
			<qdc:dcCollection xsi:schemaLocation="http://xxxxx.gelman.gwu.edu/schemas/qdc/2004/07/14/qualifieddc.xsd">
				<xsl:for-each select="marc:collection">
					<xsl:for-each select="marc:record">
						<qdc:qualifieddc>
							<xsl:apply-templates select="."/>
						</qdc:qualifieddc>
					</xsl:for-each>
				</xsl:for-each>
			</qdc:dcCollection>
		</xsl:if>
		<xsl:if test="marc:record">
			<qdc:qualifieddc xsi:schemaLocation="http://xxxxx.gelman.gwu.edu/schemas/qdc/2004/07/14/qualifieddc.xsd">
				<xsl:apply-templates/>
			</qdc:qualifieddc>
		</xsl:if>
	</xsl:template>
	
	
	<!-- ##################################################################### -->
	<!-- Main template - matches marc:record. -->
	<!-- ##################################################################### -->
	<xsl:template match="marc:record">
	
		<!-- Grab a few values for use later -->
		<xsl:variable name="leader" select="marc:leader"/>
		<xsl:variable name="leader6" select="substring($leader,7,1)"/>
		<xsl:variable name="leader7" select="substring($leader,8,1)"/>
		<xsl:variable name="controlField008" select="marc:controlfield[@tag=008]"/>
		
		
		<!-- STEP 1: TITLE MAPPING -->
		<!-- Find all 245 fields and send them out as dc:title -->
		<xsl:for-each select="marc:datafield[@tag=245]">
			<dc:title>
				<!--<xsl:call-template name="outputSubfields"/>-->
				<xsl:variable name="title-string">
					<xsl:call-template name="outputSubfields"/>
				</xsl:variable>
				<xsl:choose>
					<xsl:when test="substring($title-string,string-length($title-string),1)='/'">
						<xsl:value-of select="substring($title-string,1,string-length($title-string)-1)"/>
					</xsl:when>
					<xsl:otherwise>
						<xsl:value-of select="$title-string"/>
					</xsl:otherwise>
				</xsl:choose>
				<xsl:call-template name="getVolume"><xsl:with-param name="barcode" select="$barcode"/></xsl:call-template> 
			</dc:title>
			<!-- Look for linked alternative graphical representations -->
			<xsl:call-template name="linkedFields">
				<xsl:with-param name="element">dc:title</xsl:with-param>
			</xsl:call-template>
		</xsl:for-each>
		<!-- Find unlinked alternative graphic representations -->
		<xsl:call-template name="unlinkedFields">
			<xsl:with-param name="tags">245</xsl:with-param>
			<xsl:with-param name="element">dc:title</xsl:with-param>
		</xsl:call-template>		
		
		
		<!-- STEP 2: ALTERNATIVE TITLE MAPPING -->
		<!-- Find all 130,210,240,242,246,730,740 fields and send them out as dcterms:alternative -->
		<xsl:for-each select="marc:datafield[@tag=130] | marc:datafield[@tag=210] | marc:datafield[@tag=240] | marc:datafield[@tag=242] | marc:datafield[@tag=246] | marc:datafield[@tag=730] | marc:datafield[@tag=740]">
			<dcterms:alternative>
				<xsl:call-template name="outputSubfields"/>
			</dcterms:alternative>
			<!-- Look for alternative graphical representations -->
			<xsl:call-template name="linkedFields">
				<xsl:with-param name="element">dcterms:alternative</xsl:with-param>
			</xsl:call-template>
		</xsl:for-each>
		<!-- Find unlinked alternative graphic representations -->
		<xsl:call-template name="unlinkedFields">
			<xsl:with-param name="tags">130,210,240,242,246,730,740</xsl:with-param>
			<xsl:with-param name="element">dcterms:alternative</xsl:with-param>
		</xsl:call-template>
		
		
		<!-- STEP 3: CONTRIBUTOR MAPPING -->
		<!-- Find all 100,110,111,700,710,711,720 fields and send them out as dc:contributor elements -->
		<xsl:for-each select="marc:datafield[@tag=100] | marc:datafield[@tag=110] | marc:datafield[@tag=111] | marc:datafield[@tag=700] | marc:datafield[@tag=710] | marc:datafield[@tag=711] | marc:datafield[@tag=720]">
			<!-- Look for MARC Relator codes in subfield $e -->
			<xsl:variable name="relator">
				<xsl:value-of select="marc:subfield[@code='e']"/>
			</xsl:variable>
			<!-- create the relator element name that will be nested inside the contributor element -->
			<xsl:variable name="relatortag">
				<xsl:choose>
					<xsl:when test="string-length($relator) &gt; 0">
						<xsl:variable name="fixed-relator">
							<xsl:call-template name="fixMarcRel">
								<xsl:with-param name="relator" select="$relator"/>
							</xsl:call-template>
						</xsl:variable>
						<xsl:value-of select="concat('marcrel:',$fixed-relator)"/>
					</xsl:when>
					<!-- WARNING!!! The following logic contains a gross assumption that any unspecified 100 Main Entry is of type author. Users of this stylesheet will most likely not wish to make this kind of assumption. Simply delete the following <xsl:when> clause to remove the assumption. -->
					<xsl:when test="@tag=100 and string-length(string($relator))=0 and string-length($assumption) &gt; 0">
						<xsl:value-of select="concat('marcrel:',$assumption)"/>
					</xsl:when>
				</xsl:choose>
			</xsl:variable>
			<!-- create element -->
			<dc:contributor>
				<xsl:choose>
					<!-- If exists create the nested marc relator element and output subfield values -->
					<xsl:when test="string-length($relatortag) &gt; 0">
						<xsl:element name="{$relatortag}">
							<xsl:call-template name="outputSubfields"/>
						</xsl:element>
					</xsl:when>
					<!-- Otherwise just output the subfield values -->
					<xsl:otherwise>
						<xsl:call-template name="outputSubfields"/>
					</xsl:otherwise>
				</xsl:choose>
			</dc:contributor>
			<!-- Look for alternative graphical representations -->
			<xsl:call-template name="linkedFields">
				<xsl:with-param name="element">dc:contributor</xsl:with-param>
				<xsl:with-param name="subelement">
					<xsl:value-of select="$relatortag"/>
				</xsl:with-param>
			</xsl:call-template>
		</xsl:for-each>
		<!-- Find unlinked alternative graphic representations -->
		<xsl:call-template name="unlinkedFields">
			<xsl:with-param name="tags">100,110,111,700,710,711,720</xsl:with-param>
			<xsl:with-param name="element">dc:title</xsl:with-param>
		</xsl:call-template>
		
		
		<!-- STEP XX: SUBJECT MAPPING -->
		<!-- TODO: determine if we want all 65x fields or just those specified in LOC document -->
		<xsl:for-each select="marc:datafield[@tag=600] | marc:datafield[@tag=610] | marc:datafield[@tag=611] | marc:datafield[@tag=630] | marc:datafield[@tag=650] | marc:datafield[@tag=651] | marc:datafield[@tag=653] | marc:datafield[@tag=654] | marc:datafield[@tag=655] | marc:datafield[@tag=656] | marc:datafield[@tag=657] | marc:datafield[@tag=658]">
			<dc:subject>
				<!-- the <xsl:attribute> tag goes inside the when clause because in some cases we will not add the type attribute -->
				<xsl:choose>
					<xsl:when test="@ind2=0">
						<xsl:attribute name="xsi:type">dcterms:LCSH</xsl:attribute>
					</xsl:when>
					<xsl:when test="@ind2=2">
						<xsl:attribute name="xsi:type">dcterms:MESH</xsl:attribute>
					</xsl:when>
					<xsl:when test="@ind2=7 and marc:subfield[@code=2]='tgn'">
						<xsl:attribute name="xsi:type">dcterms:TGN</xsl:attribute>
					</xsl:when>
				</xsl:choose>
				<!-- now populate the value of the tag -->
				<xsl:call-template name="outputSubfields"/>
			</dc:subject>
		</xsl:for-each>
		
		<!-- generate subject tag for Library of Congress catalog number -->
		<xsl:for-each select="marc:datafield[@tag=050]">
			<dc:subject xsi:type="dcterms:LCC">
				<xsl:call-template name="outputSubfields"/>
			</dc:subject>
		</xsl:for-each>
		
		<!-- generate subject tag for Library of Congress catalog number -->
		<xsl:for-each select="marc:datafield[@tag=060]">
			<dc:subject xsi:type="dcterms:NLM">
				<xsl:call-template name="outputSubfields"/>
			</dc:subject>
		</xsl:for-each>
		
		<!-- generate subject tag for Dewey Decimal catalog number -->
		<xsl:for-each select="marc:datafield[@tag=082]">
			<dc:subject xsi:type="dcterms:DDC">
				<xsl:call-template name="outputSubfields"/>
			</dc:subject>
		</xsl:for-each>
		
		<!-- generate subject tag for Universal Decimal catalog number -->
		<xsl:for-each select="marc:datafield[@tag=080]">
			<dc:subject xsi:type="dcterms:UDC">
				<xsl:call-template name="outputSubfields"/>
			</dc:subject>
		</xsl:for-each>
		
		
		<!-- STEP XX: DESCRIPTION MAPPING -->
		<!-- the 500 range tags are mostly dc:description tags in the output with some exceptions -->
		<xsl:for-each select="marc:datafield[@tag &gt;=500 and @tag &lt;= 599]">
			<xsl:choose>
				<!-- Skip the following fields to avoid redundant data as they are used in other elements-->
				<xsl:when test="@tag=506 or @tag=510 or @tag=521 or @tag=530  or @tag=533 or @tag=538 or @tag=540 or @tag=541 or @tag=542 or @tag=546 or @tag=561">
					<!-- pass -->
				</xsl:when>
				<!-- the 505 tag is a table of contents entry -->
				<xsl:when test="@tag=505">
					<dcterms:tableOfConents>
						<xsl:call-template name="outputSubfields"/>
					</dcterms:tableOfConents>
				</xsl:when>
				<!-- the 520 field is an abstract if indicator 1 is set to 3 -->
				<xsl:when test="@tag=520 and @ind1=3">
					<dcterms:abstract>
						<xsl:call-template name="outputSubfields"/>
					</dcterms:abstract>
				</xsl:when>
				<xsl:otherwise>
					<dc:description>
						<xsl:call-template name="outputSubfields"/>
					</dc:description>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:for-each>
		
		
		<!-- STEP XX: LANGUAGE MAPPING -->
		<!-- Look for language code in controlfield 008 -->
		<xsl:variable name="controlFieldLang">
			<xsl:value-of select="normalize-space(substring($controlField008,36,3))"/>
		</xsl:variable>
		<xsl:if test="string-length($controlFieldLang) &gt; 0">
			<dc:language xsi:type="dcterms:ISO639-2">
				<xsl:value-of select="$controlFieldLang"/>
			</dc:language>
		</xsl:if>
		
		<!-- Look for language in 041 datafield -->
		<xsl:for-each select="marc:datafield[@tag=041]">
			<dc:language>
				<xsl:choose>
					<xsl:when test="marc:subfield[code=2]='iso639-3'">
						<xsl:attribute name="xsi:type">dcterms:ISO639-3</xsl:attribute>
					</xsl:when>
					<xsl:when test="marc:subfield[code=2]='rfc1766'">
						<xsl:attribute name="xsi:type">dcterms:RFC1766</xsl:attribute>
					</xsl:when>
					<xsl:when test="marc:subfield[code=2]='rfc3066'">
						<xsl:attribute name="xsi:type">dcterms:RFC3066</xsl:attribute>
					</xsl:when>
					<xsl:when test="marc:subfield[code=2]='rfc4646'">
						<xsl:attribute name="xsi:type">dcterms:RFC4646</xsl:attribute>
					</xsl:when>
					<xsl:otherwise>
						<xsl:attribute name="xsi:type">dcterms:ISO639-2</xsl:attribute>
					</xsl:otherwise>														
				</xsl:choose>
				<xsl:call-template name="outputSubfields"/>
			</dc:language>
		</xsl:for-each>
		
		<!-- Get language info from 546 -->
		<xsl:for-each select="marc:datafield[@tag=546]">
			<dc:language>
				<xsl:call-template name="outputSubfields"/>
			</dc:language>
		</xsl:for-each>
		
		<!-- STEP XX: PUBLISHER AND DATE MAPPING -->
		
		<!-- Get both publisher and date info from 260 field -->
		<xsl:for-each select="marc:datafield[@tag=260]">
			<!-- First check if subfields $a and $b are supplied -->
			<xsl:variable name="publisher">
				<xsl:call-template name="outputSubfields">
					<xsl:with-param name="codes">ab</xsl:with-param>
				</xsl:call-template>
			</xsl:variable>
			<!-- WARNING!!! This section has two options for mapping the publisher metadata. Choose one and comment out the other -->
			<xsl:if test="string-length($publisher) &gt; 0">
				<!-- Option 1: put the publisher info in a <dc:publisher> element -->
				<dc:publisher>
					<xsl:value-of select="$publisher"/>
				</dc:publisher>
				<!-- Look for alternative graphic representations -->
				<xsl:call-template name="linkedFields">
					<xsl:with-param name="element">dc:publisher</xsl:with-param>
				</xsl:call-template>
				<!-- Option 2: put the publisher info in a nested <dc:contributor><marcrel:pub> element -->
				<!--
				<dc:contributor>
					<marcrel:pub>
						<xsl:value-of select="$publisher"/>
					</marcrel:pub>
				</dc:contributor>
				<xsl:call-template name="linkedFields">
					<xsl:with-param name="element">dc:contributor</xsl:with-param>
					<xsl:with-param name="subelement">marcrel:pub</xsl:with-param>
				</xsl:call-template>
				-->
			</xsl:if>
			
			<!-- created tag is contained in 260$c$g -->
			<xsl:variable name="created">
				<xsl:call-template name="outputSubfields">
					<xsl:with-param name="codes">cg</xsl:with-param>
				</xsl:call-template>
			</xsl:variable>
			<xsl:if test="string-length($created) &gt; 0">
				<dcterms:created>
					<xsl:value-of select="$created"/>
				</dcterms:created>
			</xsl:if>
			<!-- issued tag is contained in 260$c and is repeatable -->
			<xsl:for-each select="marc:subfield[@code='c']">
				<dcterms:issued>
					<xsl:value-of select="."/>
				</dcterms:issued>
			</xsl:for-each>			
		</xsl:for-each>
		
		<!-- Look for unlinked alternative graphic representations of publisher data -->
		<!-- Choose between the two options for displaying the data, same as above -->
		<!-- Option 1, use <dc:publisher> element -->
		<xsl:call-template name="unlinkedFields">
			<xsl:with-param name="element">dc:publisher</xsl:with-param>
			<xsl:with-param name="tags">260</xsl:with-param>
		</xsl:call-template>
		<!-- Option 2, use nested <marcrel:pub> element -->
		<!--
		<xsl:call-template name="unlinkedFields">
			<xsl:with-param name="element">dc:contributor</xsl:with-param>
			<xsl:with-param name="subelement">marcrel:pub</xsl:with-param>
			<xsl:with-param name="tags">260</xsl:with-param>
		</xsl:call-template>
		-->
		
		<!-- Get more date info from other fields -->
		
		<!-- 533$d contains data for a created tag -->
		<xsl:for-each select="marc:datafield[@tag=533]/marc:subfield[@code='d']">
			<dcterms:created>
				<xsl:call-template name="outputSubfields"/>
			</dcterms:created>
		</xsl:for-each>
		
		<!-- chars 7 through 10 of controlfield 008 contain a created date -->
		<xsl:variable name="controlFieldDate">
			<xsl:value-of select="normalize-space(substring($controlField008,8,4))"/>
		</xsl:variable>
		<xsl:if test="string-length($controlFieldDate) &gt; 0">
			<dcterms:created>
				<xsl:value-of select="$controlFieldDate"/>
			</dcterms:created>
		</xsl:if>
		
		<!-- Get copyright data from 542 field -->
		<!-- This data may also be found in a 260 field if the date is preceded by the letter 'c'. However, this is very difficlut to parse out in XSLT 1.0 -->
		<xsl:for-each select="marc:datafield[@tag=542]">
			<dcterms:copyrighted>
				<xsl:call-template name="outputSubfields"/>
			</dcterms:copyrighted>
		</xsl:for-each>
		
		<!-- Get "modified" and "valid" data from 046 field -->
		<xsl:for-each select="marc:datafield[@tag=046]">
			<xsl:variable name="modified">
				<xsl:call-template name="outputSubfields">
					<xsl:with-param name="codes">j</xsl:with-param>
				</xsl:call-template>
			</xsl:variable>
			<xsl:variable name="valid">
				<xsl:call-template name="outputSubfields">
					<xsl:with-param name="codes">mn</xsl:with-param>
				</xsl:call-template>
			</xsl:variable>
			<xsl:if test="string-length($modified) &gt; 0">
				<dcterms:modified>
					<xsl:value-of select="$modified"/>
				</dcterms:modified>	
			</xsl:if>
			<xsl:if test="string-length($valid) &gt; 0">
				<dcterms:valid>
					<xsl:value-of select="$valid"/>
				</dcterms:valid>	
			</xsl:if>
		</xsl:for-each>


		<!-- STEP XX: TYPE MAPPING -->
		<!-- generate type information based on leader 6 and leader 7 data -->
		<xsl:if test="string-length(normalize-space($leader6))">
			<xsl:choose>
				<xsl:when test="contains('acdt', $leader6)">
					<dc:type xsi:type="dcterms:DCMIType">Text</dc:type>
				</xsl:when>
				<xsl:when test="contains('efgk', $leader6)">
					<dc:type xsi:type="dcterms:DCMIType">Image</dc:type>
				</xsl:when>
				<xsl:when test="contains('ij', $leader6)">
					<dc:type xsi:type="dcterms:DCMIType">Sound</dc:type>
				</xsl:when>
				<xsl:when test="$leader6='m'">
					<dc:type xsi:type="dcterms:DCMIType">Software</dc:type>
				</xsl:when>
				<xsl:when test="contains('opr', $leader6)">
					<dc:type xsi:type="dcterms:DCMIType">PhysicalObject</dc:type>
				</xsl:when>
			</xsl:choose>
			<!-- refined types -->
			<xsl:choose>
				<xsl:when test="contains('efk', $leader6)">
					<dc:type xsi:type="dcterms:DCMIType">StillImage</dc:type>
				</xsl:when>
				<xsl:when test="$leader6='g'">
					<dc:type xsi:type="dcterms:DCMIType">MovingImage</dc:type>
				</xsl:when>
				<xsl:when test="contains('cd', $leader6)">
					<dc:type>Notated music</dc:type>
				</xsl:when>
				<xsl:when test="$leader6='p'">
					<dc:type>Mixed material</dc:type>
				</xsl:when>
			</xsl:choose>
			<!-- even more refinement on information in leader6 -->
			<xsl:if test="contains('ef', $leader6)">
				<dc:type>Cartographic</dc:type>
			</xsl:if>
		</xsl:if>
		<!-- end checks on $leader6 -->
		<!-- leader 7 can tell us if something is a collection -->
		<xsl:if test="string-length(normalize-space($leader7))">
			<xsl:choose>
				<xsl:when test="contains('csp', $leader7)">
					<dc:type xsi:type="dcterms:DCMIType">Collection</dc:type>
				</xsl:when>
			</xsl:choose>
		</xsl:if>
		<!-- the 655 field in marc might contain DC type information -->
		<xsl:for-each select="marc:datafield[@tag=655]">
			<dc:type>
				<xsl:if test="marc:subfield[@code='2']='dct'">
					<xsl:attribute name="xsi:type">dcterms:DCMIType</xsl:attribute>
				</xsl:if>
				<xsl:call-template name="outputSubfields">
					<xsl:with-param name="codes">abcvxyz3568</xsl:with-param>
				</xsl:call-template>
			</dc:type>
		</xsl:for-each>
		
		
		<!-- STEP XX: FORMAT MAPPING -->
		<!-- get the format code -->
		<xsl:for-each select="marc:datafield[@tag=856]/marc:subfield[@code='q']">
			<dc:format xsi:type="dcterms:IMT">
				<xsl:value-of select="."/>
			</dc:format>
		</xsl:for-each>
		<!-- generate format extent tags -->
		<xsl:for-each select="marc:datafield[@tag=300]/marc:subfield[@code='a']">
			<dcterms:extent>
				<xsl:value-of select="."/>
			</dcterms:extent>
		</xsl:for-each>
		<!-- 533$e contains data for an extent tag -->
		<xsl:for-each select="marc:datafield[@tag=533]/marc:subfield[@code='e']">
			<dcterms:extent>
				<xsl:value-of select="."/>
			</dcterms:extent>
		</xsl:for-each>
		<!-- 340$a contains data about the medium -->
		<xsl:for-each select="marc:datafield[@tag=340]/marc:subfield[@code='a']">
			<dcterms:medium>
				<xsl:value-of select="."/>
			</dcterms:medium>
		</xsl:for-each>
		<!-- rest of 340 contains generic format data -->
		<xsl:for-each select="marc:datafield[@tag=340]">
			<dcterms:medium>
				<xsl:call-template name="outputSubfields"/>
			</dcterms:medium>
		</xsl:for-each>
		
		
		<!-- STEP XX: IDENTIFIER MAPPING -->
		<!-- 856$u contains the URI for the item -->
		<xsl:for-each select="marc:datafield[@tag=856]/marc:subfield[@code='u']">
			<dc:identifier xsi:type="dcterms:URI">
				<xsl:value-of select="."/>
			</dc:identifier>
		</xsl:for-each>
		
		<!-- get other ID info from 020,022,024 -->
		<!-- TODO: determine if any of these can be qualified -->
		<xsl:for-each select="marc:datafield[@tag=020]/marc:subfield[@code='a']">
			<dc:identifier>ISBN:<xsl:value-of select="."/>
			</dc:identifier>
		</xsl:for-each>
		<xsl:for-each select="marc:datafield[@tag=022]/marc:subfield[@code='a']">
			<dc:identifier>ISSN:<xsl:value-of select="."/>
			</dc:identifier>
		</xsl:for-each>
		<xsl:for-each select="marc:datafield[@tag=024]/marc:subfield[@code='a']">
			<dc:identifier>
				<xsl:value-of select="."/>
			</dc:identifier>
		</xsl:for-each>
		<!-- get Bib IDs and OCoLC IDs -->
		<xsl:for-each select="marc:datafield[@tag=035]/marc:subfield[@code='a']">
			<dc:identifier>
				<xsl:value-of select="."/>
			</dc:identifier>
		</xsl:for-each>
		
		
		<!-- STEP XX: RELATION MAPPPING -->
		<!-- Look in all fields between 760 and 787 -->
		<xsl:for-each select="marc:datafield[@tag &gt;= 760 and @tag &lt;= 787]">
			<xsl:variable name="relationNote">
				<xsl:value-of select="marc:subfield[@code='n']"/>
			</xsl:variable>
			<xsl:variable name="relationTitle">
				<xsl:value-of select="marc:subfield[@code='t']"/>
			</xsl:variable>
			<xsl:variable name="relationID">
				<xsl:value-of select="marc:subfield[@code='o']"/>
			</xsl:variable>
			<xsl:if test="string-length(concat($relationNote,$relationTitle,$relationID)) &gt; 0">
				<xsl:choose>
					<!-- relation = HasFormat -->
					<!-- WARNING!!! This field can also be mapped to <dcterms:isFormatOf>. Adjust next section as needed. -->
					<xsl:when test="@tag=776">
						<xsl:call-template name="noteUriRelation">
							<xsl:with-param name="elementName">dcterms:hasFormat</xsl:with-param>
						</xsl:call-template>
					</xsl:when>
					<!-- relation = HasPart -->
					<xsl:when test="@tag=774">
						<xsl:call-template name="noteUriRelation">
							<xsl:with-param name="elementName">dcterms:hasPart</xsl:with-param>
						</xsl:call-template>
					</xsl:when>
					<!-- relation = HasVersion -->
					<!-- WARNING!!! This field can also be mapped to <dcterms:isVersionOf>.  Adjust next section as needed. -->
					<xsl:when test="@tag=775">
						<xsl:call-template name="noteUriRelation">
							<xsl:with-param name="elementName">dcterms:hasVersion</xsl:with-param>
						</xsl:call-template>
					</xsl:when>
					<!-- relation = IsPartOf -->
					<xsl:when test="@tag=760 or @tag=773">
						<xsl:call-template name="noteUriRelation">
							<xsl:with-param name="elementName">dcterms:isPartOf</xsl:with-param>
						</xsl:call-template>
					</xsl:when>
					<!-- relation = IsReferencedBy -->
					<xsl:when test="@tag=785">
						<xsl:call-template name="noteUriRelation">
							<xsl:with-param name="elementName">dcterms:isReferencedBy</xsl:with-param>
						</xsl:call-template>
					</xsl:when>
					<!-- relation = Replaces -->
					<xsl:when test="@tag=780">
						<xsl:call-template name="noteUriRelation">
							<xsl:with-param name="elementName">dcterms:replaces</xsl:with-param>
						</xsl:call-template>
					</xsl:when>
					<!-- For fields not specified in LOC document use a generic <dc:relation> element -->
					<xsl:otherwise>
						<dc:relation>
							<xsl:call-template name="outputSubfields"/>
						</dc:relation>
					</xsl:otherwise>
				</xsl:choose>
			</xsl:if>
		</xsl:for-each>
		
		<!-- Also look in field 530 for HasFormat elements-->
		<xsl:for-each select="marc:datafield[@tag=530]">
			<xsl:call-template name="noteUriRelation">
				<xsl:with-param name="elementName">dcterms:hasFormat</xsl:with-param>
				<xsl:with-param name="noteSubfields">ab</xsl:with-param>
				<xsl:with-param name="uriSubfields">u</xsl:with-param>
			</xsl:call-template>
		</xsl:for-each>
		
		<!-- Also look in field 510 for IsReferencedBy elements-->
		<xsl:for-each select="marc:datafield[@tag=510]">
			<xsl:call-template name="noteUriRelation">
				<xsl:with-param name="elementName">dcterms:isReferencedBy</xsl:with-param>
				<xsl:with-param name="noteSubfields">abc</xsl:with-param>
				<xsl:with-param name="uriSubfields">u</xsl:with-param>
			</xsl:call-template>
		</xsl:for-each>
		
		<!-- Look in field 538 for Requires elements-->
		<xsl:for-each select="marc:datafield[@tag=538]">
			<xsl:call-template name="noteUriRelation">
				<xsl:with-param name="elementName">dcterms:requires</xsl:with-param>
				<xsl:with-param name="noteSubfields">ai</xsl:with-param>
				<xsl:with-param name="uriSubfields">u</xsl:with-param>
			</xsl:call-template>
		</xsl:for-each>
		
		<!-- Look for other IsPartOf info in 440,490,800,810,811,830, no URLs -->
		<xsl:for-each select="marc:datafield[@tag=440 or @tag=490 or @tag=800 or @tag=810 or @tag=830]">
			<dcterms:isPartOf>
				<xsl:call-template name="outputSubfields"/>
			</dcterms:isPartOf>
			<!-- Look for linked alternative graphic representations (foreign language scripts) -->
			<xsl:call-template name="linkedFields">
				<xsl:with-param name="element">dcterms:isPartOf</xsl:with-param>
			</xsl:call-template>
		</xsl:for-each>
		<!-- Look for unlinked alternative graphic representations (foreign language scripts) -->
		<xsl:call-template name="unlinkedFields">
			<xsl:with-param name="tags">440,490,800,810,811,830</xsl:with-param>
			<xsl:with-param name="element">dcterms:isPartOf</xsl:with-param>
		</xsl:call-template>
	
	
	<!-- STEP XX: COVERAGE MAPPING -->
	<!-- Look for spatial coverage in 034,255,522,650z,651,662,751,752 -->
	<xsl:for-each select="marc:datafield[@tag=255 or @tag=034 or @tag=522 or @tag=650 or @tag=651 or @tag=662 or @tag=751 or @tag=752]">
			<xsl:choose>
				<xsl:when test="@tag=650">
					<xsl:if test="marc:subfield[@code='z']">
						<dcterms:spatial>
							<xsl:value-of select="marc:subfield[@code='z']"/>
						</dcterms:spatial>
					</xsl:if>
				</xsl:when>
				<xsl:otherwise>
					<dcterms:spatial>
						<xsl:if test="@tag=651 and @ind2=7 and marc:subfield[@code='2']='tgn'">
							<xsl:attribute name="xsi:type">dcterms:TGN</xsl:attribute>
						</xsl:if>
						<xsl:call-template name="outputSubfields"/>
					</dcterms:spatial>				
				</xsl:otherwise>
			</xsl:choose>
	</xsl:for-each>
		
	<!-- 043$c contains geographic area code -->
	<!-- 044$c contains contains country of publishing code -->
	<xsl:for-each select="marc:datafield[@tag=043 or @tag=044]/marc:subfield[@code='c']">
		<dcterms:spatial xsi:type="dcterms:ISO3166">
			<xsl:value-of select="."/>
		</dcterms:spatial>
	</xsl:for-each>
	
	<!-- 033$a and 533$bcontains date/time of event -->
	<xsl:for-each select="marc:datafield[@tag=033]/marc:subfield[@code='a'] | marc:datafield[@tag=533]/marc:subfield[@code='b']">
		<dcterms:temporal>
			<xsl:value-of select="."/>
		</dcterms:temporal>
	</xsl:for-each>
	
	
	
	<!-- STEP XX: AUDIENCE MAPPING -->
	<xsl:for-each select="marc:datafield[@tag=521]">
		<dcterms:audience>
			<xsl:call-template name="outputSubfields"/>
		</dcterms:audience>
	</xsl:for-each>
	
	
	<!-- STEP XX: ACCRUAL PERIOD MAPPING -->
	<xsl:for-each select="marc:datafield[@tag=310]/marc:subfield[@code='a']">
		<dcterms:accrualPeriodicity>
			<xsl:value-of select="."/>
		</dcterms:accrualPeriodicity>
	</xsl:for-each>
	
	<!-- STEP XX: ACCRUAL METHOD MAPPING -->
	<xsl:for-each select="marc:datafield[@tag=541]/marc:subfield[@code='c']">
		<dcterms:accrualMethod>
			<xsl:value-of select="."/>
		</dcterms:accrualMethod>
	</xsl:for-each>
	

	<!-- STEP XX: PROVENANCE MAPPING -->
	<xsl:for-each select="marc:datafield[@tag=561]">
		<dcterms:provenance>
			<xsl:call-template name="outputSubfields"/>
		</dcterms:provenance>
	</xsl:for-each>
	
	
	
	<!-- STEP XX: SOURCE MAPPING -->
	<xsl:for-each select="marc:datafield[@tag=786 or @tag=534]">
		<xsl:call-template name="noteUriRelation">
			<xsl:with-param name="elementName">dc:source</xsl:with-param>
			<xsl:with-param name="noteSubfields">t</xsl:with-param>
			<xsl:with-param name="uriSubfields">o</xsl:with-param>
		</xsl:call-template>
	</xsl:for-each>
	
	
	<!-- STEP XX: RIGHTS MAPPING -->
	<xsl:for-each select="marc:datafield[@tag=506 or @tag=540]">
		<xsl:call-template name="noteUriRelation">
			<xsl:with-param name="elementName">dcterms:accessRights</xsl:with-param>
			<xsl:with-param name="noteSubfields">ad</xsl:with-param>
			<xsl:with-param name="uriSubfields">u</xsl:with-param>
		</xsl:call-template>
	</xsl:for-each>
	
	<xsl:for-each select="marc:datafield[@tag=542]">
		<xsl:call-template name="noteUriRelation">
			<xsl:with-param name="elementName">dcterms:rightsHolder</xsl:with-param>
			<xsl:with-param name="noteSubfields">abcdeflmnpr</xsl:with-param>
			<xsl:with-param name="uriSubfields">u</xsl:with-param>
		</xsl:call-template>
	</xsl:for-each>
	
	</xsl:template>
	
	
	
	
</xsl:stylesheet>

