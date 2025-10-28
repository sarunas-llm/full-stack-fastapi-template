import {
  List,
  ListItem,
  Spinner,
  Text,
  UnorderedList,
} from "@chakra-ui/react"
import { useQuery } from "@tanstack/react-query"
import { Link as RouterLink } from "@tanstack/react-router"

import { type CategoryPublic, CategoriesService } from "@/client"

interface CategoryNode extends CategoryPublic {
  children: CategoryNode[]
}

const buildCategoryTree = (categories: CategoryPublic[]): CategoryNode[] => {
  const categoryMap = new Map<string, CategoryNode>()
  const rootCategories: CategoryNode[] = []

  categories.forEach((category) => {
    const categoryId = category.id
    if (categoryId) {
      categoryMap.set(categoryId, { ...category, children: [] })
    }
  })

  categories.forEach((category) => {
    const categoryId = category.id
    if (!categoryId) return

    const node = categoryMap.get(categoryId)
    if (!node) return

    if (category.parent_category_id && categoryMap.has(category.parent_category_id)) {
      const parent = categoryMap.get(category.parent_category_id)
      parent?.children.push(node)
    } else {
      rootCategories.push(node)
    }
  })

  return rootCategories
}


const CategoryTree = ({ categories }: { categories: CategoryNode[] }) => {
  if (!categories || categories.length === 0) {
    return null
  }

  return (
    <UnorderedList>
      {categories.map((category) => (
        <ListItem key={category.id}>
          <RouterLink to={`/categories/${category.id}`}>
            {category.name}
          </RouterLink>
          <CategoryTree categories={category.children} />
        </ListItem>
      ))}
    </UnorderedList>
  )
}

const CategoryList = () => {
  const { data, isLoading, isError } = useQuery({
    queryKey: ["categories"],
    queryFn: () => CategoriesService.readCategories({}),
  })

  if (isLoading) {
    return <Spinner />
  }

  if (isError) {
    return <Text>Error loading categories.</Text>
  }

  const categoryTree = buildCategoryTree(data?.data || [])

  return <CategoryTree categories={categoryTree} />
}

export default CategoryList
