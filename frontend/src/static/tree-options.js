export const settingTreeDropdownValue = [
  { label: "Administration Tree", value: "administration" },
  { label: "Example Tree", value: "example" },
];

export const exampleTreeOptions = {
  administration: [
    {
      title: "Jawa Barat",
      value: "Jawa Barat",
      children: [
        {
          title: "Bandung",
          value: "Bandung",
        },
        {
          title: "Bogor",
          value: "Bogor",
        },
      ],
    },
    {
      title: "Yogyakarta",
      value: "Yogyakarta",
      children: [
        {
          title: "D.I Yogyakarta",
          value: "D.I Yogyakarta",
        },
        {
          title: "Sleman",
          value: "Sleman",
        },
      ],
    },
  ],
  example: [
    {
      title: "Parent #1",
      value: "parent-1",
      children: [
        {
          title: "Children #1-1",
          value: "children-1-1",
        },
        {
          title: "Children #1-2",
          value: "children-1-2",
        },
      ],
    },
    {
      title: "Parent #2",
      value: "parent-2",
      children: [
        {
          title: "Children #2-1",
          value: "children-2-1",
        },
        {
          title: "Children #2-2",
          value: "children-2-2",
        },
        {
          title: "Children #2-3",
          value: "children-2-3",
        },
      ],
    },
  ],
};
