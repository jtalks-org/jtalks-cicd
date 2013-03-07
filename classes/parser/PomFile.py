import xml.etree.ElementTree as ElementTree


class PomFile:
  """
    Represents Maven POM file and provides information inside of it. For instance we might need to get
    a version of the artifact: we need to pass a file to the class and get version:
    PomFile("pom.xml").version()

    @author stanislav bashkirtsev
  """

  # Maven XML schema, we need it to search for tags that obey this schema.
  maven_schema = "{http://maven.apache.org/POM/4.0.0}"
  tree = None

  def __init__(self, file_name):
    self.tree = ElementTree.parse(file(file_name))

  def version(self):
    """
      The version of the artifact inside of pom.xml. Note, that some modules can inherit version
      from its parents, thus version might be absent and None will be returned in this case.
    """
    version = self.get_tag_text_by_name("version")
    return version.replace("-SNAPSHOT", "")

  def artifact_id(self):
    """
      Gets the artifactId from pom.xml file. If file is not valid and there is no such tag, then None will be returned.
    """
    return self.get_tag_text_by_name("artifactId")

  def get_tag_text_by_name(self, tag_name):
    """
      Parses pom.xml file and finds the tag with specified name in it. It takes into account Maven XML schema as well.
    """
    return self.tree.getroot().findtext("{0}{1}".format(self.maven_schema, tag_name))
