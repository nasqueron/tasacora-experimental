<xsl:stylesheet version="1.0" 
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:svg="http://www.w3.org/2000/svg" 
    >
   <xsl:output method="xml" indent="yes"/>
<!--<xsl:output
method="xml"
version="1.0"
encoding="UTF-8"
omit-xml-declaration="no"
standalone="no"
indent="yes" />    -->

<!--    Copy non-relevant items -->
   <xsl:template match="@* | node()">
      <xsl:copy>
         <xsl:apply-templates select="@*|node()"/> 
      </xsl:copy>
   </xsl:template>
 
 
<!-- <xsl:variable name="forbiddenCSSchars">,:´' </xsl:variable>  -->
<!-- <xsl:variable name="forbiddenCSSchars">~!@$%^&*()+=,./';:"?><[]\{}|`# </xsl:variable>  -->
<xsl:variable name="forbiddenCSSchars">~!@$%^*()+=,./';:"?[]{}|`# &amp; &gt; &lt;</xsl:variable> 
<!-- & < -->

<!-- Replace spaces with underscores in "id" attributes to allow re-utilisation in CSS -->
   <xsl:template match="@id">
        <xsl:attribute name="id">
           <xsl:value-of select="translate(., $forbiddenCSSchars, '_')"/>
      </xsl:attribute>
   </xsl:template>
   
<!-- Replace spaces with underscores in "label" attributes to allow re-utilisation in CSS -->
   <xsl:template match="@label">
        <xsl:attribute name="id">
           <xsl:value-of select="translate(., $forbiddenCSSchars, '_')"/>
      </xsl:attribute>
   </xsl:template>   
   

<!-- Remove Style attributes -->
   <xsl:template match="@style" />
   <xsl:template match="@fill" />

   
<!-- Remove clipPath tags -->
    <xsl:template match="svg:clipPath" />
  
<!-- Remove defs tags -->
    <xsl:template match="svg:defs" /> 
  
   

</xsl:stylesheet>