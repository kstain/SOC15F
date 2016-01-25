<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl=
"http://www.w3.org/1999/XSL/Transform">
<xsl:output method="text" />
<xsl:template match="/">
<!-- declar of the class, choose based on the base class -->
<xsl:choose>
<xsl:when test="CLASS/@base">
<xsl:text>class </xsl:text><xsl:value-of select="CLASS/@name" />(<xsl:value-of select="CLASS/@base" /><xsl:text>):&#xa;</xsl:text>
</xsl:when>
<xsl:otherwise>
<xsl:text>class </xsl:text><xsl:value-of select="CLASS/@name" /><xsl:text>:&#xa;</xsl:text>
</xsl:otherwise>
</xsl:choose>
<xsl:text>  # It is an auto generated class&#xa;</xsl:text>
<!-- declar the static variables -->
<xsl:for-each select="CLASS/VAR">
<!-- choose on private variables -->
<xsl:choose>
<xsl:when test="@static='true'">
<xsl:text>  </xsl:text><xsl:if test="@private='true'"><xsl:text>__</xsl:text></xsl:if><xsl:value-of select="@name" /><xsl:text>= </xsl:text>
<xsl:choose>
<xsl:when test="text()"><xsl:value-of select="text()" /><xsl:text>&#xa;</xsl:text>
</xsl:when>
<xsl:otherwise>
<xsl:text>None&#xa;</xsl:text>
</xsl:otherwise>
</xsl:choose>
</xsl:when><xsl:otherwise/>
</xsl:choose>
</xsl:for-each>
<!-- declear non static vars in __init__ -->
<xsl:text>  def __init__(self):&#xa;</xsl:text>
<xsl:for-each select="CLASS/VAR">
<xsl:choose>
<xsl:when test="@static='true'" />
<xsl:otherwise>
<xsl:text>    self.</xsl:text><xsl:if test="@private='true'"><xsl:text>__</xsl:text></xsl:if><xsl:value-of select="@name" /><xsl:text> = </xsl:text><xsl:choose>
<xsl:when test="text()"><xsl:value-of select="text()" /><xsl:text>&#xa;</xsl:text>
</xsl:when>
<xsl:otherwise><xsl:text>None&#xa;</xsl:text>
</xsl:otherwise></xsl:choose>
</xsl:otherwise>
</xsl:choose>
</xsl:for-each><xsl:text>&#xa;</xsl:text>
<xsl:for-each select="CLASS/VAR">
<xsl:text>  def get_</xsl:text><xsl:value-of select="@name" /><xsl:text>(self):&#xa;    return self.</xsl:text><xsl:if test="@private='true'">__</xsl:if><xsl:value-of select="@name" /><xsl:text>&#xa;&#xa;</xsl:text>
<xsl:text>  def set_</xsl:text><xsl:value-of select="@name" /><xsl:text>(self, </xsl:text><xsl:value-of select="@name" /><xsl:text>):&#xa;    self.</xsl:text><xsl:if test="@private='true'">__</xsl:if><xsl:value-of select="@name" /><xsl:text> = </xsl:text><xsl:value-of select="@name" /><xsl:text>&#xa;&#xa;</xsl:text>
</xsl:for-each>
<!-- declear functions -->
<xsl:for-each select="CLASS/FUNC">
<!-- choose on class functions -->
<xsl:if test="@decorator"><xsl:text>  @</xsl:text><xsl:value-of select="@decorator" /><xsl:text>&#xa;</xsl:text></xsl:if>
<xsl:choose>
<xsl:when test="@class_method='true'">
<xsl:text>  def </xsl:text><xsl:value-of select="@name" /><xsl:text>(cls</xsl:text>
</xsl:when>
<xsl:otherwise>
<xsl:text>  def </xsl:text><xsl:value-of select="@name" /><xsl:text>(self</xsl:text>
</xsl:otherwise>
</xsl:choose><xsl:for-each select="ARG[not(text())]"><xsl:text>, </xsl:text><xsl:value-of select="@name" />
<xsl:choose>
<xsl:when test="text()"><xsl:text>=</xsl:text><xsl:value-of select="text()" />
</xsl:when>
<xsl:otherwise/>
</xsl:choose>
</xsl:for-each>
<xsl:for-each select="ARG[text()]"><xsl:text>, </xsl:text><xsl:value-of select="@name" />
<xsl:choose>
<xsl:when test="text()"><xsl:text>=</xsl:text><xsl:value-of select="text()" />
</xsl:when>
<xsl:otherwise/>
</xsl:choose>
</xsl:for-each><xsl:text>):&#xa;    # TODO: Auto-generated method stub&#xa;    pass&#xa;&#xa;</xsl:text>
</xsl:for-each>
</xsl:template>
</xsl:stylesheet>